"""This module will be used to format log messages and send them to the logs and moderation response channels"""

import discord

async def handle_moderation(message, mod_category_text, logs, azure_response, moderation_responses):
    """This function takes the messages that need moderating and handles the moderation"""
    try:
        azure_message = ""
        for res in azure_response:
            azure_message += f"name: `{res['type']}` score: `{res['severity']}`\n"
        await logs.send(f">>> {message.author} sent {message.content} in {message.channel.name} and was flagged for {mod_category_text}")
        await moderation_responses.send(f">>> Azure response: \n{azure_message}\n")

    except discord.DiscordException as e :
        print(f"was unable to return response {e}")
