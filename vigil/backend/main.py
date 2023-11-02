from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from constants import DOMAINS
from db_utils import add_data, connect_es
from dashboard import get_es_data, get_validated_class, get_package_info, summary, full_process

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://localhost",
    "https://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchQuery(BaseModel):
    type: str
    name: str
    github_token: str


@app.get("/")
async def main():
    return {"message": "Hello World"}

@app.post("/api/dashboard")
def post(search_item : SearchQuery):
    data = dict()
    es_data = get_es_data(name=search_item.name, type=search_item.type)
    if es_data:
        return { "data" : es_data}

    for domain in DOMAINS:
        p = get_validated_class(
            domain,
            name=search_item.name,
            type=search_item.type,
            github_token=search_item.github_token,
        )
        d = full_process(p)
        data[domain] = d

    data["final_score"], data["final_desc"] = summary(data)
    pkg_info = get_package_info(p)
    data["name"], data["type"], data["description"], data["url"] = (
        pkg_info["name"],
        pkg_info["type"],
        pkg_info["desc"],
        pkg_info["url"],
    )
    es = connect_es()
    res = add_data(es, data)

    return { "data" : data }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
