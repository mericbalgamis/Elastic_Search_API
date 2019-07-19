import requests, json, os
import re
from pprint import pprint
from elasticsearch import Elasticsearch, helpers
from tagDictionary import DcmTagDictionary
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

def convertTag():
    tags = DcmTagDictionary()
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".json"):
            json_data = open(filename)
            data = json.load(json_data)
            json_list = str(data)




    match = re.findall("[0-9a-fA-F]{8}",json_list)
    #print(match)


        #json_list = str(data)


    print(json.dumps(json_list, indent=4, sort_keys=True))
        #print(json_list)


        #match = re.findall(r'\d{8}', json_list)


    for p in match:
        # print(p)
        sonuc=tags.convert(p)
        #print(sonuc)
        json_list=json_list.replace(str(p),str(sonuc))

        #print(json.dumps(json_list, indent=4, sort_keys=True))


    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".json"):
            with open(filename,'w') as f:
                f.write(json.dumps(json_list, indent=5, sort_keys=True))







            #print(json_list)
            #json_list_2=data["DCMs"][1]["00080008"]


            #print(json.dumps(json_list, indent=4, sort_keys=True))
            #print(json_list)
            #print(json_list_2)

        #name=extract_values(json_list, "vr")
        #print(name)


        #if(tag in json_list):




              #print(json.dumps(json_list[element], indent=4, sort_keys=True))
             #print("true")
             #print(json.dumps(json_list[element]["00080008"], indent=4, sort_keys=True))
       # print(extract_values(json_list, "vr"))


        #print(json.dumps(json_list[element]['vr'], indent=4, sort_keys=True))
      #print(extract_values(deneme, "Value"))







    #for element in data:


        #print(tags.convert(element))

        #if('Value' in json_list[element]):
            #print(json.dumps(json_list[element]['Value'], indent=4, sort_keys=True))

            #for element in json_list[element]['Value']:
               # print((element))

                #if("{" in str(element) and ('Value' in json_list[element])):
                   # print(json_list[element]['Value'][element])



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


def main():
    es = connectElasticSearch()
    es = createIndex(es,"mr","doc")

    es = storeElasticSearch(es)
    es.indices.refresh(index="mr")


    #searchByIndex(es,"mr", "_doc", 3)


    #searchByIndex(es,"mr", "doc", 3)
    #print("asdh")

    #convertTag()
    #print("\nANOTHER QUERY EXAMPLE\n")
    #searchFullText(es, "restaurant", "neighborhood", "Manhattan")

    # Bu aramada "Roberta's Pizza" kelimesinin tümünü bulmuyor. Tekrar bakılması lazım.
    #searchFullText(es, "restaurant", "reviews", "Roberta's Pizza")

    #{"query":{"match":{"DCMs": "00080008"}}}


#startElasticSearch()
#names=extract_values('json',"vr")
#print(names)
#print(find("Value", ".json"))
#acc1 = []
#print(extract_text("00080013","acc1"))
#print(find2("00080012",".json"))
#convertTag()

#main()

