from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "localhost", "port": 9200}])
print(es.ping())