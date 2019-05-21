import os
import io, json
import pandas

def get_tool_name(string):
    my_hash = {
        "PANTHER_8.0_(all)": "PANTHER-all",
        "RBH___BBH": "RBH-BBH",
        "RSD_0.8_1e-5_Deluca": "RSD",
        "metaPhOrs": "MetaPhOrs",
        "orthoinspector_1.30_(blast_threshold_10-9)": "Orthoinspector-1.30",
        "phylomeDB": "PhylomeDB",
        "Ensembl_Compara_(e81)": "EnsemblCompara-e81",
        "Hieranoid_2": "Hieranoid2",
        "OMA_GETHOGs": "OMA-GETHOGs",
        "OMA_Groups_(RefSet5)": "OMA-Groups",
        "PANTHER_8.0_(LDO_only)": "PANTHER-LDO",
        "OMA_Pairs_(Refset5)": "OMA-Pairs",
        'EggNOG': 'EggNOG',
        'InParanoid': 'InParanoid',
        'InParanoidCore': 'InParanoidCore',
        "EggNOG_5.0_(Fine-grained)": "EggNOG-5-Fine-grained",
        "EggNOG_5.0_(Groups)": "EggNOG-5-Groups",
        "Ensembl_compara_v2": "EnsemblCompara-e56",
        "GETHOGs_2.0": "GETHOGs-2.0",
        "OMA_Groups_2.0": "OMA-Groups-2.0",
        "OMA_Pairs_2.0": "OMA-Pairs-2.0",
        "OrthoFinder_2.0_(Defaults,_with_BLAST)": "OrthoFinder-2.0-BLAST",
        "OrthoFinder_2.0_(Defaults,_with_DIAMOND)": "OrthoFinder-2.0-DIAMOND",
        "OrthoFinder_2.0_(MSA,_with_BLAST)": "OrthoFinder-2.0-MSA",
        "SonicParanoid_(default)": "SonicParanoid",
        "SonicParanoid_(fast)": "SonicParanoid_fast",
        "SonicParanoid_(sensitive)": "SonicParanoid_sensitive",
    }
    string = string.replace(" ", "_").replace("\xa0incomplete", "").replace("/", "_")
    toolname = my_hash[string]

    return toolname

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
                metric1, metric2 = "STD_comp_trees", "STD_num_orthologs"
                metric3, metric4 = "STD_RF_distance", "STD_incorrect_trees"
                index = 0
            elif method == "G_STD":
                full_method_name = "Generalized Species Tree Discordance in " + organism
                metric1, metric2 = "STD_comp_trees", "STD_num_orthologs"
                metric3, metric4 = "STD_RF_distance", "STD_incorrect_trees"
                index = 0
            elif method == "SwissTree":
                full_method_name = "Agreement with Reference Gene Phylogenies: " + method
                metric1, metric2 = "SwissTree_TPR", "SwissTree_PPV"
                metric3, metric4 = None, None
                index = 1
            elif method == "TreeFam-A":
                full_method_name = "Agreement with Reference Gene Phylogenies: " + method
                metric1, metric2 = "TreeFam-A_TPR", "TreeFam-A_PPV"
                metric3, metric4 = None, None
                index = 1
            elif method == "GOtest":
                full_method_name = "Gene Ontology Conservation Test"
                metric1, metric2 = "GOTest_ortholog_relations", "GOTest_schlicker"
                metric3, metric4 = None, None
                index = 0
            elif method == "ECtest":
                full_method_name = "Enzyme Classification Conservation Test"
                metric1, metric2 = "ECTest_ortholog_relations", "ECTest_schlicker"
                metric3, metric4 = None, None
                index = 0

            metrics_array = [
                {
                    "metrics_id": "QfO:" + metric1,
                    "tool_id": "QfO:compute_" + metric1
                },
                {
                    "metrics_id": "QfO:" + metric2,
                    "tool_id": "QfO:compute_" + metric2
                }

            ]

            if metric3 and metric4:
                metrics_array.extend([
                    {
                        "metrics_id": "QfO:" + metric3,
                        "tool_id": "QfO:compute_" + metric3
                    },
                    {
                        "metrics_id": "QfO:" + metric4,
                        "tool_id": "QfO:compute_" + metric4
                    }
                ])

            ## create dictionary with schema

            info = {

                "_id": "QfO:2011-07-07_" + challenge_id,
                "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/Challenge",
                "acronym": challenge_id,
                "name": full_method_name + " benchmark",
                "benchmarking_event_id": "QfO:2011-07-07",
                "is_automated": True,
                "dates": {
                    "creation": "2011-07-07T00:00:00Z",
                    "modification": "2011-07-07T00:00:00Z",
                    "benchmark_start": "2011-07-07T00:00:00Z",
                    "benchmark_stop": "2011-07-07T00:00:00Z"
                },
                "metrics_categories": [

                    {
                        "category": "assessment",
                        "description": "metrics used to benchmark the performance of ortholog predictors in Challenge " +
                                       full_method_name +
                                       ", generating the assessment dataset",
                        "metrics": metrics_array,
                    },
                    {
                        "category": "aggregation",
                        "description": "metrics used to aggregate the assessment data of all ortholog predictors participating in challenge " +
                                       full_method_name + " in a consolidated Aggregation dataset",
                        "metrics": [
                            {
                                "metrics_id": "QfO:aggregation",
                                "tool_id": "QfO:aggregate_benchmark"
                            }
                        ]
                    }
                ],
                "url": "https://orthology.benchmarkservice.org/cgi-bin/gateway.pl?f=CheckResults&p1=72d29d4aebb02e0d396fcad2",
                "challenge_contact_ids": [
                    "Christophe.Dessimoz",
                    "Paul.Thomas",
                    "Toni.Gabaldon",
                    "Erik.Sonnhammer"
                ],
                "references": [
                    "doi:10.1093/bib/bbr034"
    ]
            }

            ###
            # print info
            filename = "Challenge_" + challenge_id + ".json"
            # print filename

            with open(os.path.join(main_dir, out_dir, filename), 'w') as f:
                json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))

        os.chdir(main_dir)

if __name__ == "__main__":


   # Assuring the output directory does exist
    out_dir = "out/Challenges/"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    main_dir = os.getcwd()

    run(main_dir, out_dir)