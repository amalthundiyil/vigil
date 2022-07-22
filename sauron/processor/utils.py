import json
import requests


def fetch_pypi(package):
    url = "https://pypi.org/pypi/%s/json" % package
    r = requests.get(url)
    if r.status_code < 400:
        obj = r.json()
        return obj["info"]["project_urls"]["Source Code"]
    return {}


def fetch_npm(package):
    url = f"https://registry.npmjs.org/{package}" 
    r = requests.get(url)
    obj = {}
    if r.status_code < 400 and r.status_code >= 200:
        obj = r.json()
        with open("something.json", "w") as f:
            f.write(json.dumps(obj))


print(fetch_npm("depcheck"))
print(fetch_pypi("pandas"))