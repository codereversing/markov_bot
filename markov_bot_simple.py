import argparse
import collections
import discord
import random
import re

class MarkovBot(discord.Client):

    def __init__(self, args):
        discord.Client.__init__(self)

        self.token = args.token

        with open(args.inputfile) as input_file:
            text = input_file.read()

        self.markov_table = self.create_markov(text)
        self.word_list = list(self.markov_table.keys())

    def generate_sentence(self, markov_table, seed_word, num_words):
        if seed_word in markov_table:
            sentence = seed_word.capitalize()
            for i in range(0, num_words):
                next_word = random.choice(markov_table[seed_word])
                seed_word = next_word

                sentence += " " + seed_word

            return sentence
        else:
            print("Word {} not found in table.".format(seed_word))

    def create_markov(self, normalized_text):
        words = normalized_text.split()
        markov_table = collections.defaultdict(list)
        for current, next in zip(words, words[1:]):
            markov_table[current].append(next)

        return markov_table

    def run(self):
        super().run(self.token)

    async def on_ready(self):
        print("Logged on as {}!".format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return

        response = ""
        if message.content == "!talk":
            response = self.generate_sentence(self.markov_table, random.choice(self.word_list), random.randint(7, 25))

        if response:
            await message.channel.send(response)

def main(args):
    client = MarkovBot(args)
    client.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()

    required = parser.add_argument_group("required arguments")
    required.add_argument("-t", "--token", required=True)
    required.add_argument("-i", "--inputfile", required=True)

    parser._action_groups.append(optional) 
    args = parser.parse_args()

    main(args)