import json
import requests


def get_PYPI_data(package):
    url = "https://pypi.org/pypi/%s/json" % package
    r = requests.get(url)
    if r.status_code < 400:
        obj = r.json()
        return obj["info"]["project_urls"]["Source Code"]
    return {}


def get_NPM_data(package):
    url = "https://registry.npmjs.org/%s" % package
    r = requests.get(url)
    if r.status_code < 400:
        obj = r.json()
        return "https" + obj["repository"]["url"][3:]
    return {}


# get_NPM_data("depcheck")
# get_PYPI_data("pandas")
