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

data = pandas.read_csv("/home/jgarrayo/PycharmProjects/data_model/Summaries/STD/Eukaryota.tsv", sep='\t', header=0)

for i, tool in enumerate(data.iloc[:, 0]):
    participant = get_tool_name(tool)

    info = {
        "_id": "QfO:2015-01-01_P_" + participant,
        "name": "Pairwise orthologous predictions",
        "description": "List of orthologous pairs predicted by tool " + participant + " using the QfO refernce proteome dataset",
        "dates": {
            "creation": "2015-01-01T00:00:01Z",
            "modification": "2015-01-01T00:00:01Z"
        },
        "datalink": {
            "uri": "http://orthology.benchmarkservice.org/cgi-bin/gateway.pl?f=ShowProject",
            "attrs": ["archive"],
            "validation_date": "2015-01-01T00:00:01Z",
            "status": "ok"
        },
        "type": "participant",
        "access": "unknown",
        "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.4/Dataset",
        "community_id": "QfO",
        "depends_on": {
            "tool_id": "QfO:" + participant,
            "rel_dataset_ids": [
                {
                    "dataset_id": "QfO:2015-01-01_I",
                }
            ]
        },
        "version": "unknown",
        "dataset_contact_ids": [

        ]
    }

    # print info
    filename = "Dataset_participant_" + participant + ".json"
    # print filename

    with open("out/" + filename, 'w') as f:
        json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))
