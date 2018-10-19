import os
import io, json
import pandas

cancer_types = ["ACC", "BLCA", "BRCA", "CESC", "CHOL", "COAD", "DLBC", "ESCA"]

data = pandas.read_csv("../cancer_names.tsv", sep="\t",
                           comment="#", header=None)

long_names = {}
for index, row in data.iterrows():
    long_names[row[0]] = row[1]

for cancer in cancer_types:

    for participant in os.listdir("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/participants"):


        info = {
            "_id":"TCGA:2018-04-05_" + cancer + "_" + participant + "_Summary",
            "datalink":{
               "uri":"https://cancergenome.nih.gov/",
               "attrs":["archive"],
               "validation_date":"2018-04-05T00:00:00Z",
               "status":"ok"
            },
            "type":"challenge",
            "version":"unknown",
            "name":"Summary dataset for challenge: " + long_names[cancer],
            "description":"Summary dataset with information about challenge " + long_names[cancer] + " (e.g. input/output datasets, metrics...) in participant " + participant,
            "dates":{
               "creation":"2018-04-05T00:00:00Z",
               "modification":"2018-04-05T14:00:00Z"
            },
            "depends_on":{
                "tool_id": "TCGA:" + participant,
               "rel_dataset_ids": [
                            {
                                "dataset_id": "TCGA:2018-04-05_" + cancer + "_I",
                            },
                            {
                                "dataset_id": "TCGA:2018-04-05_" + cancer + "_M",
                            },
                            {
                                "dataset_id": "TCGA:2018-04-05_" + cancer + "_A_TPR_" + participant,
                            },
                            {
                                "dataset_id": "TCGA:2018-04-05_" + cancer + "_A_precision_" + participant,
                            }
                       ],
            },
            "_schema":"https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.4/Dataset",
            "community_id":"TCGA",
            "dataset_contact_ids":[
               "Matthew.Bailey",
                "Eduard.Porta",
                "Collin.Tokheim"
            ]
        }

        # print info
        filename = "Dataset_Challenge_" + cancer + "_" + participant + ".json"
        # print filename

        with open("out/" + filename, 'w') as f:
            json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))
