import json
import os
import sys

import redis
from constants import DOMAINS
from dashboard import full_process, get_package_info, get_validated_class, summary
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

Instrumentator().instrument(app).expose(app)


class SearchQuery(BaseModel):
    type: str
    name: str
    github_token: str


redis_url = os.getenv("VIGIL_REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.from_url(redis_url, decode_responses=True)


@app.get("/")
async def main():
    return {"message": "Hello World"}


# https://stackoverflow.com/a/65788650/17297103
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/dashboard")
def post(search_item: SearchQuery):
    data = dict()

    redis_key = f"{search_item.type}:{search_item.name}"
    redis_data = redis_client.get(redis_key)

    if redis_data:
        data = json.loads(redis_data)
        return {"data": data}

    for domain in DOMAINS:
        p = get_validated_class(
            domain,
            name=search_item.name,
            type=search_item.type,
            token=search_item.github_token,
        )
        d = full_process(p)
        print(d)
        data[domain] = d

    data["final_score"], data["final_desc"] = summary(data)
    pkg_info = get_package_info(p)
    data["name"], data["type"], data["description"], data["url"] = (
        pkg_info["name"],
        pkg_info["type"],
        pkg_info["desc"],
        pkg_info["url"],
    )

    json_data = json.dumps(data)
    redis_client.set(redis_key, json_data)

    return {"data": data}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
