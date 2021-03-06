import os
import io, json
import pandas

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


            info = {

                "_id": "QfO:2015-01-01_" + challenge_id + "_" + participant + "_do_summary",
                "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.4/TestAction",
                "tool_id": "QfO:" + participant,
                "action_type": "StatisticsEvent",
                "received_datasets": [
                            {
                                "dataset_id": "QfO:2015-01-01_I",
                                "role": "input"
                            },
                            {
                                "dataset_id": "QfO:2015-01-01_" + challenge_id + "_M",
                                "role": "metrics_reference"
                            },
                            {
                                "dataset_id": "QfO:2015-01-01_" + challenge_id + "_A_recall_" + participant,
                                "role": "assessment"
                            },
                            {
                                "dataset_id": "QfO:2015-01-01_" + challenge_id + "_A_precision_" + participant,
                                "role": "assessment"
                            },
                            {
                                "dataset_id": "QfO:2015-01-01_" + challenge_id + "_" + participant + "_Summary",
                                "role": "challenge"
                            }
                       ],
                "challenge_id": "QfO:2015-01-01_" + challenge_id,
                "dates":{
                   "creation": "2015-01-01T00:00:01Z",
                   "reception": "2015-01-01T00:00:01Z"
                },
                "test_contact_ids": [
                    "Christophe.Dessimoz",
                    "Paul.Thomas",
                    "Toni.Gabaldon",
                    "Erik.Sonnhammer"
                ]
            }

            # print info
            filename = "StatisticsEvent_" + challenge_id + "_" + participant + ".json"
            # print filename

            with open("../../out/" + filename, 'w') as f:
                json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))

    os.chdir(main_dir)