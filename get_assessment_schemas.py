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
        "Ensembl_Compara_(e56)": "EnsemblCompara-e56",
        "GETHOGs_2.0": "GETHOGs-2.0",
        "OMA_GETHOGs_2.0": "GETHOGs-2.0",
        "OMA_Groups_2.0": "OMA-Groups-2.0",
        "OMA_Pairs_2.0": "OMA-Pairs-2.0",
        "OrthoFinder_2.0_(Defaults,_with_BLAST)": "OrthoFinder-2.0-BLAST",
        "OrthoFinder_2.0_(Defaults,_with_DIAMOND)": "OrthoFinder-2.0-DIAMOND",
        "OrthoFinder_2.0_(MSA,_with_BLAST)": "OrthoFinder-2.0-MSA",
        "SonicParanoid_(default)": "SonicParanoid",
        "SonicParanoid_(fast)": "SonicParanoid_fast",
        "SonicParanoid_(sensitive)": "SonicParanoid_sensitive",
    }
    string = string.replace(" ", "_").replace("_(incomplete)", "").replace("/", "_")
    toolname = my_hash[string]

    return toolname

def build_json_schema (challenge_id, participant, full_method_name, metric_name, metric_value, error_value):

    info = {

        "_id": "QfO:2011-07-07_" + challenge_id + "_A_" + metric_name + "_" + participant,
        "description": "Assessment dataset for applying Metric '" + metric_name + "' to " + participant + " predictions in " +
                       full_method_name,
        "dates": {
            "creation": "2011-07-07T00:00:00Z",
            "modification": "2011-07-07T14:00:00Z"
        },
        "type": "assessment",
        "visibility": "public",
        "datalink": {
            "inline_data": {"value": metric_value, "error": error_value}
        },
        "depends_on": {
            "tool_id": "QfO:" + participant,
            "metrics_id": "QfO:" + metric_name,
            "rel_dataset_ids": [
                {
                    "dataset_id": "QfO:2011-07-07_P_" + participant,
                },
                {
                    "dataset_id": "QfO:2011-07-07_" + challenge_id + "_M",
                }
            ]
        },
        "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/Dataset",
        "community_ids": ["OEBC002"],
        "challenge_ids": ["QfO:2011-07-07_" + challenge_id],
        "version": "1",
        "name": "Assesment of " + metric_name + " in " + participant,
        "dataset_contact_ids": [
            "Christophe.Dessimoz",
            "Paul.Thomas",
            "Toni.Gabaldon",
            "Erik.Sonnhammer"
        ]
    }
    # print info
    filename = "Dataset_assessment_" + challenge_id + "_" + participant + "_" + metric_name + ".json"
    # print filename

    with open(os.path.join(main_dir, out_dir, filename), 'w') as f:
        json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))


def run(main_dir, out_dir):

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
                index = 0
            elif method == "G_STD":
                full_method_name = "Generalized Species Tree Discordance in " + organism
                metric1, metric2 = "STD-recall1", "STD-precision"
                index = 0
            elif method == "SwissTree":
                full_method_name = "Agreement with Reference Gene Phylogenies: " + method
                metric1, metric2 = "referenceSwissTree_recall", "referenceSwissTree_precision"
                index = 0
            elif method == "TreeFam-A":
                full_method_name = "Agreement with Reference Gene Phylogenies: " + method
                metric1, metric2 = "referenceTreeFam-A_recall", "referenceTreeFam-A_precision"
                index = 0
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
                    metric1, metric2 = "STD_comp_trees", "STD_num_orthologs"
                    metric3, metric4 = "STD_RF_distance", "STD_incorrect_trees"
                    value_1 = data.iloc[i, 1]
                    value_2 = data.iloc[i, 2]
                    value_3 = data.iloc[i, 3].split(' +- ')[0]
                    error_3 = data.iloc[i, 3].split(' +- ')[1]
                    value_4 = data.iloc[i, 4].split(' +- ')[0]
                    error_4 = data.iloc[i, 4].split(' +- ')[1]
                    # get the 4 assessment datasets:
                    build_json_schema(challenge_id, participant, full_method_name, metric1, value_1,
                                      0)
                    build_json_schema(challenge_id, participant, full_method_name, metric2, value_2,
                                      0)
                    build_json_schema(challenge_id, participant, full_method_name, metric3, value_3,
                                      error_3)
                    build_json_schema(challenge_id, participant, full_method_name, metric4, value_4,
                                      error_4)


                elif method == "GOtest" or method == "ECtest":
                    if method == "GOtest":
                        metric1, metric2 = "GOTest_ortholog_relations", "GOTest_schlicker"
                    elif method == "ECtest":
                        metric1, metric2 = "ECTest_ortholog_relations", "ECTest_schlicker"
                    x_value = data.iloc[i, 1]
                    y_value = data.iloc[i, 2].split(' +- ')[0]
                    x_error = 0
                    y_error = data.iloc[i, 2].split(' +- ')[1]

                    # get the 2 assessment datasets:
                    build_json_schema(challenge_id, participant, full_method_name, metric1, x_value,
                                      x_error)
                    build_json_schema(challenge_id, participant, full_method_name, metric2, y_value,
                                      y_error)

                elif method == "SwissTree" or method == "TreeFam-A":
                    metric1, metric2 = method + "_TPR", method + "_PPV"

                    x_value = data.iloc[i, 2].split(' +- ')[0]
                    y_value = data.iloc[i, 1].split(' +- ')[0]
                    x_error = data.iloc[i, 2].split(' +- ')[1]
                    y_error = data.iloc[i, 1].split(' +- ')[1]

                    # get the 2 assessment datasets:
                    build_json_schema(challenge_id, participant, full_method_name, metric1, x_value,
                                      x_error)
                    build_json_schema(challenge_id, participant, full_method_name, metric2, y_value,
                                      y_error)


        os.chdir(main_dir)


if __name__ == "__main__":


   # Assuring the output directory does exist
    out_dir = "out/assessment_datasets/"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    main_dir = os.getcwd()

    run(main_dir, out_dir)