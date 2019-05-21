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


def run(data, download_urls, main_dir, out_dir):

    for i, tool in enumerate(data.iloc[:, 0]):
        participant = get_tool_name(tool)

        info = {
            "_id": "QfO:2011-07-07_P_" + participant,
            "name": "Orthologs predicted by " + participant,
            "description": "List of orthologs pairs predicted by " + participant + " using the Quest for Orthologs reference proteome",
            "dates": {
                "creation": "2011-07-07T00:00:00Z",
                "modification": "2011-07-07T14:00:00Z"
            },
            "datalink": {
                "uri": download_urls[tool.replace(" ", "_").replace("\xa0incomplete", "").replace("/", "_")],
                "attrs": ["archive"],
                "validation_date": "2011-07-07T00:00:00Z",
                "status": "ok"
            },
            "type": "participant",
            "visibility": "public",
            "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/Dataset",
            "community_ids": ["OEBC002"],
            "challenge_ids": [
                                "QfO:2011-07-07_SwissTree",
                                "QfO:2011-07-07_STD_Fungi",
                                "QfO:2011-07-07_STD_Eukaryota",
                                "QfO:2011-07-07_GOtest",
                                "QfO:2011-07-07_TreeFam-A",
                                "QfO:2011-07-07_G_STD_Fungi",
                                "QfO:2011-07-07_G_STD_Eukaryota",
                                "QfO:2011-07-07_G_STD_LUCA",
                                "QfO:2011-07-07_G_STD_Vertebrata",
                                "QfO:2011-07-07_ECtest"
                            ],
            "depends_on": {
                "tool_id": "QfO:" + participant,
                "rel_dataset_ids": [
                    {
                        "dataset_id": "QfO:2011-07-07_I",
                    }
                ]
            },
            "version": "unknown",
            "dataset_contact_ids": [
                "aaa"
            ]
        }

        # print info
        filename = "Dataset_participant_" + participant + ".json"
        # print filename

        with open(os.path.join(main_dir, out_dir, filename), 'w') as f:
            json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))

if __name__ == "__main__":


   # Assuring the output directory does exist
    out_dir = "out/participant_datasets/"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # read file which contains download links with participant predictions
    with io.open("participant_data_urls.txt", mode='r', encoding="utf-8") as f:
        download_urls = json.load(f)

    data = pandas.read_csv(
        "/home/jgarrayo/PycharmProjects/QfO_data_model/Summaries/benchmark-events/RefSet_2011/STD/Eukaryota.tsv", sep='\t',
        header=0)

    main_dir = os.getcwd()

    run( data, download_urls, main_dir, out_dir)