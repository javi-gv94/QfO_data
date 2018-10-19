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

    info = {

         "_id":"TCGA:2018-04-05_" + cancer + "_I",
         "type":"input",
         "datalink":{
            "uri":"https://portal.gdc.cancer.gov/",
            "attrs":["archive"],
            "validation_date":"2018-04-05T00:00:00Z",
            "status":"ok"
         },
         "name": "Sequencing data from " + long_names[cancer] + " (" + cancer + ") samples",
         "description": "Input dataset for " + cancer + " cancer benchmark",
         "dates":{
            "creation":"2018-04-05T00:00:00Z",
            "modification":"2018-04-05T14:00:00Z"
         },
         "_schema":"https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.4/Dataset",
         "community_id":"TCGA",
         "version":"v12.0",
         "dataset_contact_ids":[
              "Matthew.Bailey",
              "Eduard.Porta",
              "Collin.Tokheim"
         ]

    }

    # print info
    filename = "Dataset_Input_" + cancer + ".json"
    # print filename

    with open("out/" + filename, 'w') as f:
        json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))
