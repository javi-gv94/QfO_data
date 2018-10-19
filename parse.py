from __future__ import division
import numpy as np
import pandas
import os
import io, json
import random
import gzip


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


def get_testevent_json_file(method, organism, tool, main_dir):
    if method == "STD":
        full_method_name = "Species Tree Discordance"
        event_id = "QfO:QfO4_" + method + "_" + organism + "_" + tool
    elif method == "G_STD":
        full_method_name = "Generalized Species Tree Discordance"
        event_id = "QfO:QfO4_" + method + "_" + organism + "_" + tool
    elif method == "SwissTree" or method == "TreeFam-A":
        full_method_name = "Agreement with Reference Gene Phylogenies: " + method
        event_id = "QfO:QfO4_" + method + "_" + tool
    elif method == "GOtest":
        full_method_name = "Gene Ontology Conservation Test"
        event_id = "QfO:QfO4_" + method + "_" + tool
    elif method == "ECtest":
        full_method_name = "Enzyme Classification Conservation Test"
        event_id = "QfO:QfO4_" + method + "_" + tool

    dataset_id = event_id + "_output"

    info = {
        "_id": event_id,
        "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.3/TestEvent",
        "tool_id": "QfO:" + tool,
        "input_dataset_id": "QfO:QfO4_input_seqXML",
        "output_dataset_id": dataset_id,
        "benchmarking_event_id": "QfO:QfO4_" + method,
        "dates": {
            "creation": "2015-04-14T23:59:59Z"
        }
    }

    # print info
    filename = info["_id"].split('QfO4_')[1] + "_testEvent.json"
    # print filename

    with open(main_dir + "/out/" + filename, 'w') as f:
        json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))


def get_dataset_json_file(method, organism, tool, x_value, y_value, x_error, y_error, main_dir):
    if method == "STD":
        full_method_name = "Species Tree Discordance"
        dataset_id = "QfO:QfO4_" + method + "_" + organism + "_" + tool + "_output"
    elif method == "G_STD":
        full_method_name = "Generalized Species Tree Discordance"
        dataset_id = "QfO:QfO4_" + method + "_" + organism + "_" + tool + "_output"
    elif method == "SwissTree" or method == "TreeFam-A":
        full_method_name = "Agreement with Reference Gene Phylogenies: " + method
        dataset_id = "QfO:QfO4_" + method + "_" + tool + "_output"
        organism = "unknown"
    elif method == "GOtest":
        full_method_name = "Gene Ontology Conservation Test"
        dataset_id = "QfO:QfO4_" + method + "_" + tool + "_output"
        organism = "unknown"
    elif method == "ECtest":
        full_method_name = "Enzyme Classification Conservation Test"
        dataset_id = "QfO:QfO4_" + method + "_" + tool + "_output"
        organism = "unknown"

    info = {
        "_id": dataset_id,
        "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.3/Dataset",
        "name": tool + ".tar.gz",
        "version": organism,
        "description": "Output dataset for the " + tool + " tool in the '" + full_method_name + "' benchmark event with the correspondent metrics generated from it",
        "type": "Output",
        "dates": {
            "creation": "2015-01-01T00:00:01Z",
            "modification": "2015-01-01T00:00:01Z"
        },
        # "datalink": "http://orthology.benchmarkservice.org/raw//TreeTest/Eukaryota.1f80d28e8ffd8052ddb8892e.tsv.gz",
        "dataset_contact_id": [
            "unknown"
        ]
    }

    ## add metrics item to dictionary
    if method == "STD" or method == "G_STD":
        info['metrics'] = [
            {
                "metrics_id": "QfO:STD-recall1",
                "result": {
                    "value": int(x_value)
                }
            },
            {
                "metrics_id": "QfO:STD-precision",
                "result": {
                    "value": float(y_value)
                }
            },
            {
                "metrics_id": "QfO:precision_error",
                "result": {
                    "value": float(y_error)
                }
            }
        ]
    elif method == "SwissTree" or method == "TreeFam-A":
        info['metrics'] = [
            {
                "metrics_id": "QfO:reference" + method + "_recall",
                "result": {
                    "value": float(x_value)
                }
            },
            {
                "metrics_id": "QfO:reference" + method + "_precision",
                "result": {
                    "value": float(y_value)
                }
            },
            {
                "metrics_id": "QfO:recall_error",
                "result": {
                    "value": float(x_error)
                }
            },
            {
                "metrics_id": "QfO:precision_error",
                "result": {
                    "value": float(y_error)
                }
            }
        ]
    elif method == "GOtest" or method == "ECtest":
        id = method.split("test")[0]
        info['metrics'] = [
            {
                "metrics_id": "QfO:" + id + "ConservationTest-recall",
                "result": {
                    "value": int(x_value)
                }
            },
            {
                "metrics_id": "QfO:" + id + "ConservationTest-precision",
                "result": {
                    "value": float(y_value)
                }
            },
            {
                "metrics_id": "QfO:precision_error",
                "result": {
                    "value": float(y_error)
                }
            }
        ]

    # print info
    filename = info["_id"].split('QfO4_')[1] + ".json"
    # print filename

    with open(main_dir + "/out/" + filename, 'w') as f:
        json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))


main_dir = os.getcwd()
for method in os.listdir(main_dir + "/Summaries/"):
    if method == ".DS_Store":
        os.remove(main_dir + "/Summaries/.DS_Store")
        continue
    os.chdir(os.getcwd() + "/Summaries/" + method)
    for filename in os.listdir(os.getcwd()):
        if filename == ".DS_Store":
            os.remove(filename)
            continue
        data = pandas.read_csv(filename, sep='\t', header=0)
        if method == "STD" or method == "G_STD":
            organism = filename.split('.')[0]
            for i, tool in enumerate(data.iloc[:, 0]):
                toolname = get_tool_name(tool)
                x_value = data.iloc[i, 1]
                y_value = data.iloc[i, 3].split(' +- ')[0]
                x_error = 0
                y_error = data.iloc[i, 3].split(' +- ')[1]
                # print tool, x_value, y_value, error
                get_dataset_json_file(method, organism, toolname, x_value, y_value, x_error, y_error, main_dir)
                get_testevent_json_file(method, organism, toolname, main_dir)
        elif method == "GOtest" or method == "ECtest":
            organism = ""
            for i, tool in enumerate(data.iloc[:, 0]):
                toolname = get_tool_name(tool)
                x_value = data.iloc[i, 1]
                y_value = data.iloc[i, 2].split(' +- ')[0]
                x_error = 0
                y_error = data.iloc[i, 2].split(' +- ')[1]
                # print tool, x_value, y_value, error
                get_dataset_json_file(method, organism, toolname, x_value, y_value, x_error, y_error, main_dir)
                get_testevent_json_file(method, organism, toolname, main_dir)
        else:
            organism = ""
            for i, tool in enumerate(data.iloc[:, 1]):
                toolname = get_tool_name(tool)
                x_value = data.iloc[i, 3].split(' +- ')[0]
                y_value = data.iloc[i, 2].split(' +- ')[0]
                x_error = data.iloc[i, 3].split(' +- ')[1]
                y_error = data.iloc[i, 2].split(' +- ')[1]
                # print x_value,x_error,toolname,y_value,y_error
                get_dataset_json_file(method, organism, toolname, x_value, y_value, x_error, y_error, main_dir)
                get_testevent_json_file(method, organism, toolname, main_dir)
        # print (method, organism)
    os.chdir(main_dir)


virtualenv .pyenv
  790  source .pyenv/bin/activate
  791  pip install -r requirements.txt
  792  python jsonValidate.py ../../json-schemas ../../prototype-data/Qfo_total/
  793  clear
