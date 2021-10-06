import argparse
import os
import re
import string
import validators

def normalize_text(line):
    if not line:
        return ""

    trimmed_line = " ".join(line.split())
    split_line = ""
    for word in trimmed_line.split(" "):
        if validators.url(word):
            continue

        split_line += word.lower() + " "

    if not split_line or split_line.isspace():
        return ""

    pattern = re.compile(r"[^A-Za-z ]+", re.UNICODE)
    normalized_line = pattern.sub("", split_line)

    return normalized_line

def main(args):
    print("Reading input file {}. Writing output to {}.".format(args.inputfile, args.outputfile));

    with open(args.outputfile, "w+", encoding="utf-8") as output_file:
        with open(args.inputfile, encoding="utf-8") as input_file:
            for input_line in input_file:
                output_line = normalize_text(input_line.rstrip())
                if output_line: 
                    output_file.write(output_line)

    print("Finished processing.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()

    required = parser.add_argument_group("required arguments")
    required.add_argument("-i", "--inputfile", required=True)

    optional.add_argument("-o", "--outputfile", nargs="?")

    parser._action_groups.append(optional) 
    args = parser.parse_args()

    main(args)
