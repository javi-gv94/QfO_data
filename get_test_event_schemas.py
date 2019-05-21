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


def run(data, main_dir, out_dir):

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

            for i, tool in enumerate(data.iloc[:, 0]):
                participant = get_tool_name(tool)

                info = {


                        "_id": "QfO:2011-07-07_testEvent_" + challenge_id + "_" + participant,
                        "_schema":"https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/TestAction",
                        "action_type":"TestEvent",
                        "tool_id":"QfO:" + participant,
                        "involved_datasets":[
                           {
                              "dataset_id": "QfO:2011-07-07_I",
                              "role": "incoming"
                           },
                           {
                                "dataset_id": "QfO:2011-07-07_P_" + participant,
                                "role": "outgoing"
                           }

                        ],
                        "challenge_id": "QfO:2011-07-07_" + challenge_id,
                        "dates":{
                           "creation": "2011-07-07T00:00:00Z",
                           "reception": "2011-07-07T00:00:00Z",
                        },
                        "test_contact_ids": [
                            "Christophe.Dessimoz",
                            "Paul.Thomas",
                            "Toni.Gabaldon",
                            "Erik.Sonnhammer"
                        ]
                }

                # print info
                filename = "TestEvent_" + challenge_id + "_" + participant + ".json"
                # print filename

                with open(os.path.join(main_dir, out_dir, filename), 'w') as f:
                    json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))

        os.chdir(main_dir)

if __name__ == "__main__":


   # Assuring the output directory does exist
    out_dir = "out/test_events/"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    data = pandas.read_csv(
        "/home/jgarrayo/PycharmProjects/QfO_data_model/Summaries/benchmark-events/RefSet_2011/STD/Eukaryota.tsv", sep='\t',
        header=0)

    main_dir = os.getcwd()

    run( data, main_dir, out_dir)