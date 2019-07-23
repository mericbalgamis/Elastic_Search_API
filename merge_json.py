import requests, json, os
import re
from pprint import pprint
from elasticsearch import Elasticsearch, helpers
from tagDictionary import DcmTagDictionary
import json



name="1.2.752.24.7.2268657091.254554-e5141679-66c8-4f2f-97c0-2b7735e2ab79-2019-05-09_03-11-54"
input_name = name+".json"
output_name=name+"_test_out.json"

#rule result altındaki rule idlerin success edenleri sırayla gezilecek her birimnin sop uid degerine bakılarak
# input jsonında hangi resme karşılık geldiği anlaşılacak ve oraya gömülecek




   # f.write(json.dumps(json_list, indent=5, sort_keys=True))





with open(output_name) as json_file:
    data = json.load(json_file)
    for i in range(0, 40):
        for p in data['individual_results'][0]['rule_results'][0]['SUCCESS'][i]["SOP_Instance_UID"]["Value"]:#value degerleri
            value = p

    #for p in data['individual_results'][0]['rule_results']:
            print(json.dumps(value, indent=5, sort_keys=True))
            #print(data)
    for i in range(0, 40):
        for k in data['individual_results'][0]['rule_results'][0]['SUCCESS'][i]["rule_id"]:#rule id
             print(k)


#verilen tage göre input jsonı guncellemek  icin
a_dict = {'rule_id': 00}

with open(input_name) as f:
    data = json.load(f)

data.update(a_dict)
for p in data['DCMs']:
    with open(input_name, 'w') as f:
         json.dump(data, f)


    # for p in data['DCMs']:
    # print(json.dumps(p, indent=5, sort_keys=True))




