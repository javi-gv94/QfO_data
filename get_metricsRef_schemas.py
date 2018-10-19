import os
import io, json


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
            url = "http://orthology.benchmarkservice.org"
            index = 0
        elif method == "G_STD":
            full_method_name = "Generalized Species Tree Discordance"
            metric1, metric2 = "STD-recall1", "STD-precision"
            url = "http://orthology.benchmarkservice.org"
            index = 0
        elif method == "SwissTree":
            full_method_name = "Agreement with Reference Gene Phylogenies: " + method
            metric1, metric2 = "referenceSwissTree_recall", "referenceSwissTree_precision"
            url = "https://swisstree.vital-it.ch/species_tree"
            index = 1
        elif method == "TreeFam-A":
            full_method_name = "Agreement with Reference Gene Phylogenies: " + method
            metric1, metric2 = "referenceTreeFam-A_recall", "referenceTreeFam-A_precision"
            url = "http://www.treefam.org/"
            index = 1
        elif method == "GOtest":
            full_method_name = "Gene Ontology Conservation Test"
            metric1, metric2 = "GOConservationTest-recall", "GOConservationTest-precision"
            index = 0
            url = "https://www.ebi.ac.uk/GOA"
        elif method == "ECtest":
            full_method_name = "Enzyme Classification Conservation Test"
            metric1, metric2 = "ECConservationTest-recall", "ECConservationTest-precision"
            url = "https://enzyme.expasy.org/"
            index = 0


        info = {
            "_id": "QfO:2015-01-01_" + challenge_id + "_M",
            "datalink": {
                "uri": url,
                "attrs": ["archive"],
                "validation_date": "2015-01-01T00:00:01Z",
                "status": "ok"
            },
            "type": "metrics_reference",
            "version": "unknown",
            "name": "Metrics Reference Dataset for " + full_method_name,
            "description": "------------------------------------------------------------- ",
            "dates": {
                "creation": "2015-01-01T00:00:01Z",
                "modification": "2015-01-01T00:00:01Z"
            },
            "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.4/Dataset",
            "community_id": "QfO",
            "dataset_contact_ids": [
                "Christophe.Dessimoz",
                "Paul.Thomas",
                "Toni.Gabaldon",
                "Erik.Sonnhammer"
            ]
        }

        # print info
        filename = "Dataset_Metrics_Ref_" + challenge_id + ".json"
        # print filename

        with open("../../out/" + filename, 'w') as f:
            json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))

    os.chdir(main_dir)


