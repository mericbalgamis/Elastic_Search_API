import requests, json, os
import re
from pprint import pprint
from elasticsearch import Elasticsearch, helpers
from tagDictionary import DcmTagDictionary
from collections import defaultdict
import json
from pprint import pprint

#00080018

class OutputObject(object):
    def __init__(self, rule_id, SOP):
        self.rule_id = rule_id,
        self.SOP = SOP


name="1.2.752.24.7.2268657091.254554-e5141679-66c8-4f2f-97c0-2b7735e2ab79-2019-05-09_03-11-54"
input_name = name+".json"
output_name=name+"_test_out.json"

#rule result altındaki rule idlerin success edenleri sırayla gezilecek her birimnin sop uid degerine bakılarak
# input jsonında hangi resme karşılık geldiği anlaşılacak ve oraya gömülecek




   # f.write(json.dumps(json_list, indent=5, sort_keys=True))


output_list = []


# output json SOP_Instance_UID degerleri
with open(output_name) as json_file:
    output = json.load(json_file)
    for i in range(0, len(output['individual_results'][0]['rule_results'])):
        for j in range(0, len(output['individual_results'][0]['rule_results'][i]['SUCCESS'])):
            for p in output['individual_results'][0]['rule_results'][0]['SUCCESS'][j]["SOP_Instance_UID"]["Value"]:
                output_rule_id = output['individual_results'][0]['rule_results'][i]["rule_id"]
                output_SOP = p

                output_list.append(OutputObject(output_rule_id,output_SOP))

#for obj in output_list:
    #print(obj.rule_id)

with open(input_name,"r+") as json_file:
    input = json.load(json_file)
    for i in range(0, len(input['DCMs'])):
        for input_SOP in input['DCMs'][i]["00080018"]["Value"]:
            for output_obj in output_list:
                if(input_SOP==output_obj.SOP):

                    a_dict = {'SUCCESS':{"rule_id":output_obj.rule_id}}



                    #print(output_obj.rule_id)

                    #with open(input_name) as f:
                        #data = json.load(f)

                    input['DCMs'][i].update(a_dict)

                    with open(input_name, 'w') as f:
                          json.dump(input, f)







    #for p in data['individual_results'][0]['rule_results']:
            #print(json.dumps(output_SOP, indent=5, sort_keys=True))
            #print(data)
#    for i in range(0, 40):
#        for k in data['individual_results'][0]['rule_results'][0]['SUCCESS'][i]["rule_id"]:#rule id
#             print(k)


#verilen tage göre input jsonı guncellemek  icin
#a_dict = {'rule_id': 00}

#with open(input_name) as f:
#    data = json.load(f)

#data.update(a_dict)
#for p in data['DCMs']:
#    with open(input_name, 'w') as f:
#         json.dump(data, f)


    # for p in data['DCMs']:
    # print(json.dumps(p, indent=5, sort_keys=True))




