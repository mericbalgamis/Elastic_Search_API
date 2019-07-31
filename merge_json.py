import json


class individualObject(object):
    def __init__(self, rule_id, SOP, subset_id):
        self.rule_id = rule_id
        self.SOP = SOP
        self.subset_id = subset_id


class mandatoryObject(object):
    def __init__(self, rule_id, SOP, subset_id):
        self.rule_id = rule_id
        self.SOP = SOP
        self.subset_id = subset_id


class optionalObject(object):
    def __init__(self, rule_id, SOP, subset_id):
        self.rule_id = rule_id
        self.SOP = SOP
        self.subset_id = subset_id


class recommendedObject(object):
    def __init__(self, rule_id, SOP, subset_id):
        self.rule_id = rule_id
        self.SOP = SOP
        self.subset_id = subset_id


# {
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
# }

name = "1.2.752.24.7.2268657091.254554-e5141679-66c8-4f2f-97c0-2b7735e2ab79-2019-05-09_03-11-54"
input_name = name + ".json"
output_name = name + "_test_out.json"
individual_list = []
mandatory_list = []
recommended_list = []
optional_list = []

# rule result altindaki rule idlerin success edenleri sirasiyla gezilecek her birimnin sop uid degerine bakilarak


# 00080018


# output json SOP_Instance_UID degerleri
with open(output_name) as json_file:
    output = json.load(json_file)
    for i in range(0, len(output['individual_results'][0]['rule_results'])):
        for j in range(0, len(output['individual_results'][0]['rule_results'][i]['SUCCESS'])):
            for p in output['individual_results'][0]['rule_results'][0]['SUCCESS'][j]["SOP_Instance_UID"]["Value"]:
                output_rule_id = output['individual_results'][0]['rule_results'][i]["rule_id"]
                output_SOP = p
                output_subset_id = output['individual_results'][0]['subset_id']

                individual_list.append(individualObject(output_rule_id, output_SOP, output_subset_id))

# output json bulk_result success degerleri mandatory
with open(output_name) as json_file:
    output = json.load(json_file)
    for i in range(0, len(output['bulk_results'][0]['mandatory']['SUCCESS'])):
        for j in range(0, len(output['bulk_results'][0]['mandatory']['SUCCESS'][i]['SUCCESS'])):
            for p in output['bulk_results'][0]['mandatory']['SUCCESS'][i]['SUCCESS'][j]["SOP_Instance_UID"]["Value"]:
                mandatory_rule_id = output['bulk_results'][0]['mandatory']['SUCCESS'][i]['SUCCESS'][j]["rule_id"]
                mandatory_SOP_value = p
                mandatory_subset_id = output['bulk_results'][0]['subset_id']

                mandatory_list.append(mandatoryObject(mandatory_rule_id, mandatory_SOP_value, mandatory_subset_id))

# output json bulk_result success degerleri optional
with open(output_name) as json_file:
    output = json.load(json_file)
    for i in range(0, len(output['bulk_results'][0]['optional']['SUCCESS'])):
        for j in range(0, len(output['bulk_results'][0]['optional']['SUCCESS'][i]['SUCCESS'])):
            for p in output['bulk_results'][0]['optional']['SUCCESS'][i]['SUCCESS'][j]["SOP_Instance_UID"]["Value"]:
                optional_rule_id = output['bulk_results'][0]['optional']['SUCCESS'][i]['SUCCESS'][j]["rule_id"]
                optional_SOP_value = p
                optional_subset_id = output['bulk_results'][0]['subset_id']

                optional_list.append(optionalObject(optional_rule_id, optional_SOP_value, optional_subset_id))

# output json bulk_result success degerleri recommended
with open(output_name) as json_file:
    output = json.load(json_file)
    for i in range(0, len(output['bulk_results'][0]['recommended']['SUCCESS'])):
        for j in range(0, len(output['bulk_results'][0]['recommended']['SUCCESS'][i]['SUCCESS'])):
            for p in output['bulk_results'][0]['recommended']['SUCCESS'][i]['SUCCESS'][j]["SOP_Instance_UID"]["Value"]:
                recommended_rule_id = output['bulk_results'][0]['recommended']['SUCCESS'][i]['SUCCESS'][j]["rule_id"]
                recommended_SOP_value = p
                recommended_subset_id = output['bulk_results'][0]['subset_id']

                recommended_list.append(
                    recommendedObject(recommended_rule_id, recommended_SOP_value, recommended_subset_id))

# input jsona SOP_Instance_UID degerlerine göre rule id lerin append edilmesi
with open(input_name, "r+") as json_file:
    input = json.load(json_file)
    for i in range(0, len(input['DCMs'])):
        for input_SOP in input['DCMs'][i]["00080018"]["Value"]:

            b_dict = {
                "SUCCESS": {
                    "individual_results": {
                        "subset_id": [

                        ],
                        "rule_id": [

                        ]
                    },
                    "bulk_results": {
                        "subset_id": [

                        ],


                        "mandatory": {
                            "rule_id": []
                        },
                        "optional": {
                            "rule_id": []
                        },
                        "recommended": {
                            "rule_id": []
                        }
                    }
                }
            }
            input['DCMs'][i].update(b_dict)

            for output_obj in individual_list:
                if (input_SOP == output_obj.SOP):
                    input['DCMs'][i]['SUCCESS']['individual_results']['rule_id'].append(output_obj.rule_id)

                    input['DCMs'][i]['SUCCESS']['individual_results']['subset_id'].append(output_obj.subset_id)

            # input['DCMs'][i].update(b_dict)

            for output_obj in mandatory_list:
                if (input_SOP == output_obj.SOP):
                    input['DCMs'][i]['SUCCESS']['bulk_results']['mandatory']['rule_id'].append(output_obj.rule_id)

                    input['DCMs'][i]['SUCCESS']['bulk_results']['subset_id'].append(output_obj.subset_id)

            for output_obj in optional_list:
                if (input_SOP == output_obj.SOP):
                    input['DCMs'][i]['SUCCESS']['bulk_results']['optional']['rule_id'].append(output_obj.rule_id)

            for output_obj in recommended_list:
                if (input_SOP == output_obj.SOP):
                    input['DCMs'][i]['SUCCESS']['bulk_results']['recommended']['rule_id'].append(output_obj.rule_id)

        with open(input_name, 'w') as f:
            json.dump(input, f)