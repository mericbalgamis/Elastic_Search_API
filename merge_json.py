import json

class individualObject(object):
    def __init__(self, rule_id, SOP):
        self.rule_id = rule_id
        self.SOP = SOP

class mandatoryObject(object):
    def __init__(self, rule_id, SOP):
        self.rule_id = rule_id
        self.SOP = SOP

class optionalObject(object):
    def __init__(self, rule_id, SOP):
        self.rule_id = rule_id
        self.SOP = SOP

class recommendedObject(object):
    def __init__(self, rule_id, SOP):
        self.rule_id = rule_id
        self.SOP = SOP

#{
#    "SUCCESS": {
#        "individual_results": {
#            "rule_id": [
#                ""
#            ]
#        },
#        "bulk_results": {
#            "mandatory": {
#                "rule_id": [
#                    ""
#                ]
#            },
#            "optional": {
#                "rule_id": [
#                    ""
#                ]
#            },
#            "recommended": {
#                "rule_id": [
#                    ""]
#            }
#        }
#    }
#}

name="1.2.752.24.7.2268657091.254554-e5141679-66c8-4f2f-97c0-2b7735e2ab79-2019-05-09_03-11-54"
input_name = name+".json"
output_name=name+"_test_out.json"
output_list = []

#rule result altındaki rule idlerin success edenleri sırayla gezilecek her birimnin sop uid degerine bakılarak
# input jsonında hangi resme karşılık geldiği anlaşılacak ve oraya gömülecek

#00080018


# output json SOP_Instance_UID degerleri
with open(output_name) as json_file:
    output = json.load(json_file)
    for i in range(0, len(output['individual_results'][0]['rule_results'])):
        for j in range(0, len(output['individual_results'][0]['rule_results'][i]['SUCCESS'])):
            for p in output['individual_results'][0]['rule_results'][0]['SUCCESS'][j]["SOP_Instance_UID"]["Value"]:
                output_rule_id = output['individual_results'][0]['rule_results'][i]["rule_id"]
                output_SOP = p

                output_list.append(individualObject(output_rule_id,output_SOP))

# input jsona SOP_Instance_UID degerlerine göre rule id lerin append edilmesi
with open(input_name,"r+") as json_file:
    input = json.load(json_file)
    for i in range(0, len(input['DCMs'])):
        for input_SOP in input['DCMs'][i]["00080018"]["Value"]:
            for output_obj in output_list:
                if(input_SOP==output_obj.SOP):
                    if('SUCCESS' in input['DCMs'][i]):
                        input['DCMs'][i]['SUCCESS']['rule_id'].append(output_obj.rule_id)
                        print(input['DCMs'][i]['SUCCESS']['rule_id'])

                        with open(input_name, 'w') as f:
                            json.dump(input, f)

                    else:
                        a_dict = {'SUCCESS': {"rule_id": [output_obj.rule_id]}}
                        #a_dict = {'SUCCESS': {["rule_id": [output_obj.rule_id]}}
                        input['DCMs'][i].update(a_dict)

                        with open(input_name, 'w') as f:
                            json.dump(input, f)



