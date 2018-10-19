import os
import io, json


cancer_types = ["ACC", "BLCA", "BRCA", "CESC", "CHOL", "COAD", "DLBC", "ESCA"]

for cancer in cancer_types:

    for participant in os.listdir("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/participants"):


        info = {

            "_id": "TCGA:2018-04-05_" + cancer + "_" + participant + "_do_summary",
            "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.4/TestAction",
            "tool_id": "TCGA:" + participant,
            "action_type": "StatisticsEvent",
            "received_datasets": [
                        {
                            "dataset_id": "TCGA:2018-04-05_" + cancer + "_I",
                            "role": "input"
                        },
                        {
                            "dataset_id": "TCGA:2018-04-05_" + cancer + "_M",
                            "role": "metrics_reference"
                        },
                        {
                            "dataset_id": "TCGA:2018-04-05_" + cancer + "_A_TPR_" + participant,
                            "role": "assessment"
                        },
                        {
                            "dataset_id": "TCGA:2018-04-05_" + cancer + "_A_precision_" + participant,
                            "role": "assessment"
                        },
                        {
                            "dataset_id": "TCGA:2018-04-05_" + cancer + "_" + participant + "_Summary",
                            "role": "challenge"
                        }
                   ],
            "challenge_id": "TCGA:2018-04-05_" + cancer,
            "dates":{
               "creation": "2018-04-05T00:00:00Z",
               "reception": "2018-04-05T00:00:00Z"
            },
            "test_contact_ids": [
                "Matthew.Bailey",
                "Eduard.Porta",
                "Collin.Tokheim"
            ]
        }

        # print info
        filename = "StatisticsEvent_" + cancer + "_" + participant + ".json"
        # print filename

        with open("out/" + filename, 'w') as f:
            json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))
