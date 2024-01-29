# pylint: disable=import-error disable=unused-variable disable=line-too-long
import os
import discord
import commands
import responses
import handle_moderation
import azure_moderation
import gcp_moderation
from dotenv import load_dotenv
load_dotenv()

async def send_message(message, user_message, is_private, flag):
    """This function will respond with what the user sent in the channel, This is a test function"""
    try:
        if flag:
            response = responses.handle_responses(user_message, flag)
            handle_message = message.author.send(response) if is_private else await message.channel.send(response)
            delete_message = await message.delete()
            print("This message has been removed")
        else:
            response = responses.handle_responses(user_message, flag)
            handle_message = message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(f"was un able to return response {e}")

async def handle_command(message, user_message):
    """This function handles the commands for the users, commands are
    defined within the commands.py file
    """
    command = str(user_message).split()[0][1:]
    print(command)
    if command == "clear":
        limit = 5
        get_limit = str(user_message).split()
        if len(get_limit) == 2:
            limit = int(get_limit[1])
        else:
            message.channel.send("The command should be clear (number to clear)")
        await commands.clear_command(limit, message.channel)
    else:
        await message.channel.send("This is not a recognised command")



def run_discord_bot():
    """This is the main function for running the bot"""
    intents = discord.Intents.all()
    token = os.environ["bot_token"]
    # print(TOKEN)
    client = discord.Client(intents=intents)


    @client.event
    async def on_ready():
        print(f'{client.user} is ready!')

    @client.event
    async def on_message(message):

        # This stops the bot from replying to itself
        if message.author == client.user:
            return

        logs = ""
        moderation_responses=""
        for server in client.guilds:
            for channel in server.channels:
                if str(channel.type) == 'text' and channel.name == "logs":
                    logs = channel
                elif str(channel.type) == 'text' and channel.name == "moderation-responses":
                    moderation_responses = channel

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        azure_response = azure_moderation.azure_text_moderation(user_message)
        gcp_response = await gcp_moderation.gcp_text_moderation(user_message)

        flag = False
        # This creates a string for the log message
        new_text = ""
        for res in azure_response:
            new_text += f'{res["type"]}, '
        new_text = new_text[:-2]
        # Here we set the flag true if the message has been moderated use this flag to handle the moderation.
        if len(azure_response) > 0:
            flag = True
        print(f"{username} sent {user_message} in {channel}")

        if user_message[0] == "!":
            await handle_command(message, user_message)
        elif flag:
            await handle_moderation.handle_moderation(message, new_text, is_private=False, flag=flag, logs=logs, azure_response=azure_response, gcp_response=gcp_response, moderation_responses=moderation_responses)
        else:
            await send_message(message, user_message, is_private=False, flag=flag)
    client.run(token)
