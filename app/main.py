"""This is the entry point for running the bot"""

import bot

config = {}
raw_config = open("config.txt", "r", encoding="UTF8")
for line in raw_config:
    if line != "\n":
        line_split = line.replace('\n', "").replace(" ", "").lower().split("=")
        config.update({line_split[0]: int(line_split[1])})

bot.run_discord_bot(config=config)
