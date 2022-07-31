from secrets import token_hex
import json

from elasticsearch import Elasticsearch, helpers
import requests

from sauron.processor.base_processor import validate
from sauron.processor.base_backend import BackendTypes, BackendUrls


def add_data(es, data):
    if es.indices.exists("sauron"):
        r = es.indices.create("sauron", ignore=400)
    res = es.index(index="sauron", doc_type="sauron", body=data)
    return res


def get_data(url, name, type, es):
    validate(url, name, type)
    es.indices.refresh(index="sauron")
    if url:
        es_d = es.search(index="sauron", query={"match": {"url": url}})
        if es_d and es_d["hits"] and es_d["hits"]["hits"]:
            return es_d["hits"]["hits"][0]["_source"]
    elif name and type:
        if type == BackendTypes.github:
            owner = name.split("/")[0]
            repo = name.split("/")[1]
            q = {
                "bool": {
                    "must": [
                        {"term": {"type": type}},
                    ]
                }
            }
            es_d = es.search(index="sauron", query=q)
            if es_d and es_d["hits"] and es_d["hits"]["hits"]:
                data = es_d["hits"]["hits"]
                for d in data:
                    if d["_source"]["name"] == name:
                        return d["_source"]
        else:
            es_d = es.search(
                index="sauron",
                query={
                    "bool": {
                        "must": [
                            {"term": {"name": name}},
                            {"term": {"type": type}},
                        ]
                    }
                },
            )
            if es_d and es_d["hits"] and es_d["hits"]["hits"]:
                return es_d["hits"]["hits"][0]["_source"]


def drop_data(es):
    r = es.indices.delete(index="sauron", ignore=[400, 404])
    return r
