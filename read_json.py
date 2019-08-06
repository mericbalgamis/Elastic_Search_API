import json, os
import re
from pprint import pprint
from elasticsearch import Elasticsearch
from tagDictionary import DcmTagDictionary
import sys

first = True
path_input = "/merged_inputs/"
path_output = "/merged_inputs_outputs/"
global form_type

form_type=sys.argv[1]
#print(sys.argv[1])

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

def keys_exists(element, *keys):
    '''
    Check if *keys (nested) exists in `element` (dict).
    '''
    if type(element) is not dict:
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True
# Function for creating index in Elastic Search
def createIndex(es, index_name,type_name):

    doc={
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

def convertTag(name):

    tags = DcmTagDictionary()
    path = "merged_inputs_outputs/"

    json_data = open(path+name+".json")
    data = json.load(json_data)
    json_list = str(data)
    match = re.findall("'[0-9]{8}':",json_list)

    for p in match:
        p = p[1:-2]
        sonuc=tags.convert(p)
        json_list = json_list.replace("'", "\"")
        json_list=json_list.replace(p,sonuc)

    json_str = "'" + json_list + "'"
    final_dictionary = eval(json_str)

    with open(path+name+".json", "w") as f:
        f.write(final_dictionary)

# Establish connection to elastic search and returns ES object
def extract_text(obj, acc):
         if isinstance(obj, dict):
            for k, v in obj.items():
             if isinstance(v, (dict, list)):
                 extract_text(v, acc)
             elif k == "text":
                    acc.append(v)
         elif isinstance(obj, list):
             for item in obj:
                 extract_text(item, acc)


def connectElasticSearch():

    es = Elasticsearch([{'host': 'localhost', 'port': 9200}],sniff_on_start=True)
    #es.indices.create(index='restaurant')

    # returns true if connection is successful
    if es.ping():
        print('Elasticsearch connected')
    else:
        print('Elasticsearch could not connect!')

    return es

def find(key, dictionary):
    for k, v in dictionary.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result

# Search for JSON files in cwd and store JSON files in Elastic Search
def storeElasticSearch(es):
    #print("store")
    path = ""
    global path_input
    global path_output
    #print("store* " + form_type)
    if(form_type != "input"):
        path = path_output
        #print("store+ "+form_type)
    else:
        path = path_input
        print("store- " + form_type)

    i = 1
    if es is not None:
        for filename in os.listdir(os.getcwd()+path):
            if filename.endswith(".json"):
                f = open(os.getcwd()+path+filename)
                docket_content = f.read()

                # Send the data into es
                es.index(index='mr', ignore=400, id=i, body=json.loads(docket_content),request_timeout=50)
                print('Data indexed successfully')
                i = i+1

    return es

def startElasticSearch(var):
    es = connectElasticSearch()
    if first:
        es.indices.delete(index='mr', ignore=[400, 404])
        es = createIndex(es, "mr", "doc")
        es = storeElasticSearch(es)
        setFalse()

    es.indices.refresh(index="mr")
    form_type = str(var)
    #print("start+ "+form_type)
    return es


def find2(key, dictionary):
    for k, v in dictionary.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                if isinstance(d, dict):
                    for result in find(key, d):
                        yield result
def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

def setFalse():
    global first
    first = False

def convertMergedInputs():
    for filename in os.listdir(os.getcwd() + "/merged_inputs_outputs"):
        if filename.endswith(".json"):
            print(filename[:-5])
            convertTag(filename[:-5])

def main():

    es = connectElasticSearch()
    es = createIndex(es,"mr","doc")

    es = storeElasticSearch(es)
    es.indices.refresh(index="mr")
