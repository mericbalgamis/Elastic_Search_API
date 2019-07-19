import requests, json, os
from pprint import pprint
from elasticsearch import Elasticsearch, helpers
import logging

first = True

# Simple search function for elastic search
def searchFullText(es, index_name, name, value):

    search_body = {'query':
                       {'match':
                            {name: value}
                       }
                  }

    res = es.search(index=index_name, body=search_body)
    pprint(res['hits']['hits'])
    #pprint(res)


def searchByIndex(es_object, index_name, type, id):

    res = es_object.get(index=index_name, doc_type=type, id=id)
    return res
    #pprint(res)


# Function for creating index in Elastic Search
def createIndex(es, index_name,type_name):
    doc = {

        "settings" : {
            "index" : {
                "number_of_shards" : 1,
                "number_of_replicas" : 1
            }
        }
    }


    res = es.index(index=index_name,doc_type=type_name,body=doc)
    print(res['result'])
    return es

def convertTag():
    print("xfbds")
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".json"):
            f = open(filename)
            json_file = f.read()
            print(json_file['DCMs'])


# Establish connection to elastic search and returns ES object
def connectElasticSearch():

    es = Elasticsearch([{'host': 'localhost', 'port': 9200}],sniff_on_start=True)
    #es.indices.create(index='restaurant')

    # returns true if connection is successful
    if es.ping():
        print('Elasticsearch connected')
    else:
        print('Elasticsearch could not connect!')

    return es

# Search for JSON files in cwd and store JSON files in Elastic Search
def storeElasticSearch(es):
    print("store")
    i = 1
    if es is not None:
        for filename in os.listdir(os.getcwd()):
            if filename.endswith(".json"):
                f = open(filename)
                docket_content = f.read()

                # Send the data into es
                es.index(index='mr', ignore=400, id=i, body=json.loads(docket_content),request_timeout=50)
                print('Data indexed successfully')
                i = i+1

    return es

def startElasticSearch():
    es = connectElasticSearch()
    if first:
        es = createIndex(es, "mr", "doc")
        es = storeElasticSearch(es)
        setFalse()
    es.indices.refresh(index="mr")

    return es

def setFalse():
    global first
    first = False

def main():
    es = connectElasticSearch()
    es = createIndex(es,"mr","doc")

    es = storeElasticSearch(es)
    es.indices.refresh(index="mr")

    #searchByIndex(es,"mr", "doc", 3)
    #print("asdh")
    #convertTag()
    #print("\nANOTHER QUERY EXAMPLE\n")
    #searchFullText(es, "restaurant", "neighborhood", "Manhattan")

    # Bu aramada "Roberta's Pizza" kelimesinin tümünü bulmuyor. Tekrar bakılması lazım.
    #searchFullText(es, "restaurant", "reviews", "Roberta's Pizza")

    #{"query":{"match":{"DCMs": "00080008"}}}

#main()