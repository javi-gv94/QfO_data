from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-i", "--data", help="raw data", required=True)
parser.add_argument("-i2", "--data2", help="raw data 2", required=False)
parser.add_argument("-o", "--out_file", help="out file name", required=True)
parser.add_argument("-c", "--challenge", help="challenge name", required=True)


args = parser.parse_args()

input_path = args.data
input_path_2 = args.data2
out_file = args.out_file
challenge = args.challenge


fp = open(input_path, 'r')

line = fp.readline()
count = 0

participant_name = None
if challenge == "ECtest" or challenge == "GOtest":
    while line:

        if line.startswith("#"):
            participant_name = line.replace('# ', '').strip()
        elif line != "" and line[0].isdigit():
            values = line.split("\t")
            tsv_entry = "\t".join([participant_name, values[0], values[1] + " +- " + values[2]])
            out_f = open(out_file, "a+")
            out_f.write(tsv_entry)
            out_f.close()

        line = fp.readline()

elif challenge == "Swisstree" or challenge == "Treefam-A":

    while line:

        if line.startswith("#"):
            participant_name = line.replace('# ', '').strip()
        elif line != "" and line[0].isdigit():
            values = line.split("\t")
            tsv_entry = "\t".join([participant_name, values[1] + " +- " + values[3],  values[2] + " +- " + values[4]])
            out_f = open(out_file, "a+")
            out_f.write(tsv_entry)
            out_f.close()

        line = fp.readline()

elif challenge == "STD" or challenge == "G_STD":

    file2 = open(input_path_2, 'r')
    file2_lines = file2.readlines()

    while line:

        if line.startswith("#"):
            participant_name = line.replace('# ', '').strip()
            if line.startswith("# pareto points"):
                break
        elif line != "" and line[0].isdigit():
            values = line.split("\t")
            values2 = file2_lines[count].split("\t")

            tsv_entry = "\t".join([participant_name, values[0], values2[0], values[1] + " +- " + values[2].rstrip(),  values2[1] + " +- " + values2[2]])
            out_f = open(out_file, "a+")
            out_f.write(tsv_entry)
            out_f.close()

        line = fp.readline()
        count += 1

fp.close()