import argparse
import collections
import os.path
import random
import re
import sys

def generate_sentence(markov_table, seed_word, num_words):
    if seed_word in markov_table:
        sentence = seed_word.capitalize()
        for i in range(0, num_words):
            next_word = random.choice(markov_table[seed_word])
            seed_word = next_word

            sentence += " " + seed_word

        return sentence
    else:
        print("Word {} not found in table.".format(seed_word))

def create_markov(normalized_text):
    words = normalized_text.split()
    markov_table = collections.defaultdict(list)
    for current, next in zip(words, words[1:]):
        markov_table[current].append(next)

    return markov_table

def normalize_text(raw_text):
    pattern = re.compile(r"[^a-zA-Z0-9- ]")
    normalized_text = pattern.sub("", raw_text.replace("\n", " ")).lower()
    normalized_text = " ".join(normalized_text.split())

    return normalized_text

def main(args):
    if not os.path.exists(args.inputfile):
        print("File {} does not exist.".format(args.inputfile))
        sys.exit(-1)

    with open(args.inputfile, "r", encoding="utf-8") as input_file:
        normalized_text = normalize_text(input_file.read())

    model = create_markov(normalized_text)
    generated_sentence = generate_sentence(model, normalize_text(args.seed), args.numwords)

    print(generated_sentence)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()

    required = parser.add_argument_group("required arguments")
    required.add_argument("-i", "--inputfile", required=True)
    required.add_argument("-s", "--seed", required=True)

    optional.add_argument("-n", "--numwords", nargs="?", default=int(30))

    parser._action_groups.append(optional) 
    args = parser.parse_args()

    main(args)