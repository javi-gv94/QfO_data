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

        datasets = []
        tools = []
        datasets.append({
            "dataset_id": "QfO:2015-01-01_I",
            "role": "input"
        })
        datasets.append({
            "dataset_id": "QfO:2015-01-01_" + challenge_id + "_M",
            "role": "metrics_reference"
        })

        data = pandas.read_csv(name, sep='\t', header=0)

        for i, tool in enumerate(data.iloc[:, index]):

            participant = get_tool_name(tool)
            tools.append({"tool_id": "QfO:" + participant})

            datasets.append({
                "dataset_id": "QfO:2015-01-01_" + challenge_id + "_P_" + participant,
                "role": "participant"
            })
            datasets.append({
                "dataset_id": "QfO:2015-01-01_" + challenge_id + "_A_recall_" + participant,
                "role": "assessment"
            })
            datasets.append({
                "dataset_id": "QfO:2015-01-01_" + challenge_id + "_A_precision_" + participant,
                "role": "assessment"
            })

            datasets.append({
                "dataset_id": "QfO:2015-01-01_" + challenge_id + "_" + participant + "_Summary",
                "role": "challenge"
            })

        info = {

            "_id": "QfO:2015-01-01_" + challenge_id,
            "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.4/Challenge",
            "name": full_method_name + " benchmark",
            "benchmarking_event_id": "QfO:2015-01-01",
            "is_automated": True,
            "dates": {
                    "creation": "2015-01-01T00:00:01Z",
                    "modification": "2015-01-01T00:00:01Z",
                    "benchmark_start": "2015-01-01T00:00:01Z",
                    "benchmark_stop": "2015-04-14T23:59:59Z"
            },
            "dataset_ids": datasets,
            "participants": tools,
            "metrics": [
                {
                    "metrics_id": "QfO:" + metric1
                },
                {
                    "metrics_id": "QfO:" + metric2
                },
                {
                    "metrics_id": "QfO:recall_error"
                },
                {
                    "metrics_id": "QfO:precision_error"
                },

            ],
            "url": "http://orthology.benchmarkservice.org/cgi-bin/gateway.pl?f=CheckResults&p1=72d29d4aebb02e0d396fcad2",
            "community_id": "QfO",
            "challenge_contact_ids": [
                "Christophe.Dessimoz",
                "Paul.Thomas",
                "Toni.Gabaldon",
                "Erik.Sonnhammer"
            ],
            "references": [
                "10.1038/nmeth.3830"
            ]
        }

        ###
        # print info
        filename = "Challenge_" + challenge_id + ".json"
        # print filename

        with open("../../out/" + filename, 'w') as f:
            json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))

    os.chdir(main_dir)