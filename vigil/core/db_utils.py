from secrets import token_hex
import json
import sys
from tkinter import E
from urllib.parse import urlparse

from elasticsearch import Elasticsearch, helpers

from base.processor import validate
from base.backend import BackendTypes, BackendUrls


def connect_es(elastic_url=None):
    if elastic_url:
        url = urlparse(elastic_url)
        es = Elasticsearch([{"host": url.hostname, "port": url.port}])
    else:
        es = Elasticsearch([{"host": "localhost", "port": 9200}])
    if not es.ping():
        click.secho("❗ Could not connect to elastic search!", fg="red", bold=True)
        return None
    return es


def add_data(es, data):
    if es.indices.exists("vigil"):
        r = es.indices.create("vigil", ignore=400)
    res = es.index(index="vigil", doc_type="vigil", body=data)
    return res


def iterate_over_items(es, type, key, value):
    es_d = es.search(index="vigil", query={"match_all": {}})
    if es_d and es_d["hits"] and es_d["hits"]["hits"]:
        data = es_d["hits"]["hits"]
        for d in data:
            if d["_source"][key] == value:
                return d["_source"]


def get_db_data(url, name, type, es):
    validate(url, name, type)
    if not es.indices.exists("vigil"):
        return
    es.indices.refresh(index="vigil")
    if url:
        return iterate_over_items(es, type, "url", url)
    elif name and type:
        if type == BackendTypes.github:
            return iterate_over_items(es, type, "url", url)
        else:
            return iterate_over_items(es, type, "name", name)


def drop_data(es):
    r = es.indices.delete(index="vigil", ignore=[400, 404])
    return r
