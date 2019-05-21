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

def build_json_schema (challenge_id, participant, metric_name):
    info = {

        "_id": "QfO:2011-07-07_" + challenge_id + "_metricsEvent_" + participant + "_" + metric_name,
        "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/TestAction",
        "action_type": "MetricsEvent",
        "tool_id": "QfO:" + participant,
        "involved_datasets": [
            {
                "dataset_id": "QfO:2011-07-07_" + challenge_id + "_M",
                "role": "incoming"
            },
            {
                "dataset_id": "QfO:2011-07-07_P_" + participant,
                "role": "incoming"
            },
            {
                "dataset_id": "QfO:2011-07-07_" + challenge_id + "_A_" + metric_name + "_" + participant,
                "role": "outgoing"
            }
        ],
        "challenge_id": "QfO:2011-07-07_" + challenge_id,
        "dates": {
            "creation": "2011-07-07T00:00:00Z",
            "reception": "2011-07-07T00:00:00Z"
        },
        "test_contact_ids": [
            "Christophe.Dessimoz",
            "Paul.Thomas",
            "Toni.Gabaldon",
            "Erik.Sonnhammer"
        ]
    }
    # print info
    filename = "MetricsEvent_" + challenge_id + "_" + participant + "_" + metric_name + ".json"
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


            ## create dictionary with schema


            data = pandas.read_csv(name, sep='\t', header=0)

            for i, tool in enumerate(data.iloc[:, 0]):

                participant = get_tool_name(tool)

                if method == "STD":
                    full_method_name = "Species Tree Discordance in " + organism
                    metric1, metric2 = "STD_comp_trees", "STD_num_orthologs"
                    metric3, metric4 = "STD_RF_distance", "STD_incorrect_trees"
                    build_json_schema(challenge_id, participant, metric1)
                    build_json_schema(challenge_id, participant, metric2)
                    build_json_schema(challenge_id, participant, metric3)
                    build_json_schema(challenge_id, participant, metric4)

                elif method == "G_STD":
                    full_method_name = "Generalized Species Tree Discordance in " + organism
                    metric1, metric2 = "STD_comp_trees", "STD_num_orthologs"
                    metric3, metric4 = "STD_RF_distance", "STD_incorrect_trees"
                    build_json_schema(challenge_id, participant, metric1)
                    build_json_schema(challenge_id, participant, metric2)
                    build_json_schema(challenge_id, participant, metric3)
                    build_json_schema(challenge_id, participant, metric4)

                elif method == "SwissTree":
                    full_method_name = "Agreement with Reference Gene Phylogenies: " + method
                    metric1, metric2 = "SwissTree_TPR", "SwissTree_PPV"
                    build_json_schema(challenge_id, participant, metric1)
                    build_json_schema(challenge_id, participant, metric2)

                elif method == "TreeFam-A":
                    full_method_name = "Agreement with Reference Gene Phylogenies: " + method
                    metric1, metric2 = "TreeFam-A_TPR", "TreeFam-A_PPV"
                    build_json_schema(challenge_id, participant, metric1)
                    build_json_schema(challenge_id, participant, metric2)

                elif method == "GOtest":
                    full_method_name = "Gene Ontology Conservation Test"
                    metric1, metric2 = "GOTest_ortholog_relations", "GOTest_schlicker"
                    build_json_schema(challenge_id, participant, metric1)
                    build_json_schema(challenge_id, participant, metric2)

                elif method == "ECtest":
                    full_method_name = "Enzyme Classification Conservation Test"
                    metric1, metric2 = "ECTest_ortholog_relations", "ECTest_schlicker"
                    build_json_schema(challenge_id, participant, metric1)
                    build_json_schema(challenge_id, participant, metric2)


        os.chdir(main_dir)

if __name__ == "__main__":


   # Assuring the output directory does exist
    out_dir = "out/metrics_events/"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    main_dir = os.getcwd()

    run(main_dir, out_dir)