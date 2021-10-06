import argparse
import dateutil.parser
import sys
import time

import discord

class ScraperClient(discord.Client):
    
    def __init__(self, args):
        discord.Client.__init__(self)

        self.token = args.token
        self.channel_id = int(args.channel)

        self.last_date = dateutil.parser.parse(args.date)
        self.output_path = args.outputfile

    def run(self):
        super().run(self.token)

    async def get_chat_history(self, channel, output_path, last_date):
        with open(output_path , "w+", encoding="utf-8") as output_file:
            async for message in channel.history(limit=None, after=last_date):
                output = message.content + "\n"
                output_file.write(output)

    async def on_ready(self):
        print("Logged on as {}!".format(self.user))

        channel = self.get_channel(self.channel_id)
        if channel is None:
            print("Could not find channel {}".format(self.channel_id))
            sys.exit(-1)

        print("Found channel #{} for id {}. Reading messages...".format(channel.name, self.channel_id))
        with open(self.output_path , "w+", encoding="utf-8") as output_file:
            await self.get_chat_history(channel, self.output_path, self.last_date)

        print("Finished reading messages.")
        sys.exit(0)

def main(args):
    client = ScraperClient(args)
    client.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()

    required = parser.add_argument_group("required arguments")
    required.add_argument("-c", "--channel", required=True)
    required.add_argument("-t", "--token", required=True)

    optional.add_argument("-d", "--date", nargs="?", default="2015-01-10 00:00:00")
    optional.add_argument("-o", "--outputfile", nargs="?", default="output-{}.out".format(int(time.time())))

    parser._action_groups.append(optional) 
    args = parser.parse_args()

    main(args)