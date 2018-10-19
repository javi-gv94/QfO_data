import os
import io, json
import pandas
from datauri import DataURI



def get_tool_name(string):
    my_hash = {
        "PANTHER_8.0_(all)": "PANTHER-all",
        "RBH___BBH": "RBH-BBH",
        "RSD_0.8_1e-5_Deluca": "RSD",
        "metaPhOrs": "MetaPhOrs",
        "orthoinspector_1.30_(blast_threshold_10-9)": "Orthoinspector",
        "phylomeDB": "PhylomeDB",
        "Ensembl_Compara_(e81)": "EnsemblCompara",
        "Hieranoid_2": "Hieranoid2",
        "OMA_GETHOGs": "OMA-GETHOGs",
        "OMA_Groups_(RefSet5)": "OMA-Groups",
        "PANTHER_8.0_(LDO_only)": "PANTHER-LDO",
        "OMA_Pairs_(Refset5)": "OMA-Pairs",
        'EggNOG': 'EggNOG',
        'InParanoid': 'InParanoid',
        'InParanoidCore': 'InParanoidCore'
    }
    string = string.replace(" ", "_").replace("\xa0incomplete", "").replace("/", "_")
    toolname = my_hash[string]

    return toolname


main_dir = os.getcwd()
for method in os.listdir(main_dir + "/Summaries/"):
    if method == ".DS_Store":
        os.remove(main_dir + "/Summaries/.DS_Store")
        continue
    os.chdir(os.getcwd() + "/Summaries/" + method)

    for name in os.listdir(os.getcwd()):
        if name == ".DS_Store":
            os.remove(name)
            continue

        organism = name.split('.')[0]

        # compose challenge id
        if organism == "Eukaryota" or organism == "Fungi" or organism == "Vertebrata" or organism == "LUCA":
            challenge_id = method + "_" + organism
        else:
            challenge_id = method

        # set method name and metrics
        if method == "STD":
            full_method_name = "Species Tree Discordance"
            metric1, metric2 = "STD-recall1", "STD-precision"
            index = 0
        elif method == "G_STD":
            full_method_name = "Generalized Species Tree Discordance"
            metric1, metric2 = "STD-recall1", "STD-precision"
            index = 0
        elif method == "SwissTree":
            full_method_name = "Agreement with Reference Gene Phylogenies: " + method
            metric1, metric2 = "referenceSwissTree_recall", "referenceSwissTree_precision"
            index = 1
        elif method == "TreeFam-A":
            full_method_name = "Agreement with Reference Gene Phylogenies: " + method
            metric1, metric2 = "referenceTreeFam-A_recall", "referenceTreeFam-A_precision"
            index = 1
        elif method == "GOtest":
            full_method_name = "Gene Ontology Conservation Test"
            metric1, metric2 = "GOConservationTest-recall", "GOConservationTest-precision"
            index = 0
        elif method == "ECtest":
            full_method_name = "Enzyme Classification Conservation Test"
            metric1, metric2 = "ECConservationTest-recall", "ECConservationTest-precision"
            index = 0

        ## create dictionary with schema


        data = pandas.read_csv(name, sep='\t', header=0)

        for i, tool in enumerate(data.iloc[:, index]):
            participant = get_tool_name(tool)
            if method == "STD" or method == "G_STD":

                    x_value = data.iloc[i, 1]
                    y_value = data.iloc[i, 3].split(' +- ')[0]
                    x_error = 0
                    y_error = data.iloc[i, 3].split(' +- ')[1]

            elif method == "GOtest" or method == "ECtest":

                    x_value = data.iloc[i, 1]
                    y_value = data.iloc[i, 2].split(' +- ')[0]
                    x_error = 0
                    y_error = data.iloc[i, 2].split(' +- ')[1]

            else:

                    x_value = data.iloc[i, 3].split(' +- ')[0]
                    y_value = data.iloc[i, 2].split(' +- ')[0]
                    x_error = data.iloc[i, 3].split(' +- ')[1]
                    y_error = data.iloc[i, 2].split(' +- ')[1]

            #get data-uri value of the 2 metrics
            metric_value_1 = DataURI.make('application/json', charset='us-ascii', base64=True, data=json.dumps(x_value))
            metric_value_2 = DataURI.make('application/json', charset='us-ascii', base64=True, data=json.dumps(y_value))

            #print metrics1 assesment file
            info = {
               "_id":"QfO:2015-01-01_" + challenge_id + "_A_recall_" + participant,
               "description":"Assessment dataset of applying Metric " + metric1 + " to " + participant + " ortholog predictions",
               "dates":{
                  "creation": "2015-01-01T00:00:01Z",
                  "modification": "2015-01-01T00:00:01Z"
               },
               "type":"assessment",
               "datalink":{
                  "uri":metric_value_1,
                  "attrs":["inline"],
                  "status":"ok",
                  "validation_date":"2015-01-01T00:00:01Z"
               },
               "depends_on":{
                  "tool_id":"QfO:" + participant,
                  "metrics_id":"QfO:" + metric1,
                  "rel_dataset_ids":[
                     {
                        "dataset_id":"QfO:2015-01-01_I",
                     },
                     {
                        "dataset_id":"QfO:2015-01-01_" + challenge_id + "_M",
                     }
                  ]
               },
               "_schema":"https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.4/Dataset",
               "community_id":"QfO",
               "version":"1",
               "name":"Assesment of Metric " + metric1 + " in " + participant,
               "dataset_contact_ids":[
                  "Christophe.Dessimoz",
                    "Paul.Thomas",
                    "Toni.Gabaldon",
                    "Erik.Sonnhammer"
               ]
            }

            # print info
            filename = "Dataset_assessment_" + challenge_id + "_" + participant + "_recall.json"
            # print filename

            with open("../../out/" + filename, 'w') as f:
                json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))

            # print metrics2 assessment file
            info = {
                "_id": "QfO:2015-01-01_" + challenge_id + "_A_precision_" + participant,
                "description": "Assessment dataset of applying Metric " + metric2 + " to " + participant + " ortholog predictions",
                "dates": {
                    "creation": "2015-01-01T00:00:01Z",
                    "modification": "2015-01-01T00:00:01Z"
                },
                "type": "assessment",
                "datalink": {
                    "uri": metric_value_2,
                    "attrs": ["inline"],
                    "status": "ok",
                    "validation_date": "2015-01-01T00:00:01Z"
                },
                "depends_on": {
                    "tool_id": "QfO:" + participant,
                    "metrics_id": "QfO:" + metric2,
                    "rel_dataset_ids": [
                        {
                            "dataset_id": "QfO:2015-01-01_I",
                        },
                        {
                            "dataset_id": "QfO:2015-01-01_" + challenge_id + "_M",
                        }
                    ]
                },
                "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.4/Dataset",
                "community_id": "QfO",
                "version": "1",
                "name": "Assesment of Metric " + metric2 + " in " + participant,
                "dataset_contact_ids": [
                    "Christophe.Dessimoz",
                    "Paul.Thomas",
                    "Toni.Gabaldon",
                    "Erik.Sonnhammer"
                ]
            }

            # print info
            filename = "Dataset_assessment_" + challenge_id + "_" + participant + "_precision.json"
            # print filename

            with open("../../out/" + filename, 'w') as f:
                json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))
    os.chdir(main_dir)