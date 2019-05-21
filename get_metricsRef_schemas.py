import os
import io, json


def run (main_dir, out_dir):

    for method in os.listdir(main_dir + "/Summaries/benchmark-events/RefSet_2011/"):
        if method == ".DS_Store":
            os.remove(main_dir + "/Summaries/benchmark-events/RefSet_2011/.DS_Store")
            continue
        os.chdir(os.getcwd() + "/Summaries/benchmark-events/RefSet_2011/" + method)
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
                full_method_name = "Species Tree Discordance in " + organism
                metric1, metric2 = "STD-recall1", "STD-precision"
                url = "http://orthology.benchmarkservice.org"
                description = organism + " Species Tree that can be used in the Species Tree Discordance benchmark as reference " \
                              "to assess the accuracy of orthologs predicted"
                index = 0
            elif method == "G_STD":
                full_method_name = "Generalized Species Tree Discordance in " + organism
                metric1, metric2 = "STD-recall1", "STD-precision"
                url = "http://orthology.benchmarkservice.org"
                description = organism + " Species Tree that can be used in the Generalized Species Tree Discordance benchmark " \
                              "as reference to assess the accuracy of orthologs predicted"
                index = 0
            elif method == "SwissTree":
                full_method_name = "Agreement with Reference Gene Phylogenies: " + method
                metric1, metric2 = "referenceSwissTree_recall", "referenceSwissTree_precision"
                url = "https://swisstree.vital-it.ch/species_tree"
                description = "Gene Tree that can be used in the SwissTree benchmark as reference to assess the " \
                              "accuracy of orthologs predicted"
                index = 1
            elif method == "TreeFam-A":
                full_method_name = "Agreement with Reference Gene Phylogenies: " + method
                metric1, metric2 = "referenceTreeFam-A_recall", "referenceTreeFam-A_precision"
                url = "http://www.treefam.org/"
                description = "Gene Tree that can be used in the TreeFam-A benchmark as reference to assess the " \
                              "accuracy of orthologs predicted"
                index = 1
            elif method == "GOtest":
                full_method_name = "Gene Ontology Conservation Test"
                metric1, metric2 = "GOConservationTest-recall", "GOConservationTest-precision"
                index = 0
                url = "https://www.ebi.ac.uk/GOA"
                description = "Functional Annotations from the Uniprot-Gene Ontology Annotation (GOA) database that " \
                              "can be used in the Gene Ontology Conservation benchmark as reference to assess the accuracy of orthologs predicted"
            elif method == "ECtest":
                full_method_name = "Enzyme Classification Conservation Test"
                metric1, metric2 = "ECConservationTest-recall", "ECConservationTest-precision"
                url = "https://enzyme.expasy.org/"
                index = 0
                description = "Functional Annotations from the Enzyme Commission (EC) numbers database that can be used " \
                              "in the Enzyme Classification Conservation benchmark as reference to assess the accuracy of orthologs predicted"


            info = {
                        "_id":"QfO:2011-07-07_" + challenge_id + "_M",
                        "datalink":{
                           "uri":url,
                           "attrs":["archive"],
                           "validation_date":"2011-07-07T00:00:00Z",
                           "status":"ok"
                        },
                        "type":"metrics_reference",
                        "challenge_ids": ["QfO:2011-07-07_" + challenge_id],
                        "visibility": "community",
                        "version":"unknown",
                        "name":"Metrics Reference Dataset for " + full_method_name + " benchmark",
                        "description":description,
                        "dates":{
                           "creation":"2011-07-07T00:00:00Z",
                           "modification":"2011-07-07T14:00:00Z"
                        },
                        "depends_on":{
                           "rel_dataset_ids":[
                                  {
                                     "dataset_id": "QfO:2011-07-07_I",
                                  }
                               ]
                        },
                        "_schema":"https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/Dataset",
                        "community_ids":["OEBC002"],
                        "dataset_contact_ids":[
                           "Christophe.Dessimoz",
                            "Paul.Thomas",
                            "Toni.Gabaldon",
                            "Erik.Sonnhammer"
                        ]
                    }

            # print info
            filename = "Dataset_Metrics_Ref_" + challenge_id + ".json"
            # print filename

            with open(os.path.join(main_dir, out_dir, filename), 'w') as f:
                json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))

        os.chdir(main_dir)


if __name__ == "__main__":


   # Assuring the output directory does exist
    out_dir = "out/reference_datasets/"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    main_dir = os.getcwd()

    run(main_dir, out_dir)


