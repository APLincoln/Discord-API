# pylint: disable=import-error disable=unused-variable disable=line-too-long
import discord
import commands
import responses
from dotenv import load_dotenv
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions
import os

load_dotenv()

def azure_text_moderation(mod_text):
    """This function will take the message and send it to the azure content safety api"""
    endpoint = os.environ["endpoint"]
    key=os.environ["azure_token"]
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request= AnalyzeTextOptions(text=mod_text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("Analyze image failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise
    result = []
    if response.hate_result.severity >= 2:
        print(f"Hate severity: {response.hate_result.severity}")
        result.append({"severity": response.hate_result.severity, "type": "Hate"})
    if response.self_harm_result.severity >= 2:
        print(f"SelfHarm severity: {response.self_harm_result.severity}")
        result.append({"severity": response.self_harm_result.severity, "type": "SelfHarm"})
    if response.sexual_result.severity >= 2:
        print(f"Sexual severity: {response.sexual_result.severity}")
        result.append({"severity": response.sexual_result.severity, "type": "Sexual"})
    if response.violence_result.severity >= 2:
        print(f"Violence severity: {response.violence_result.severity}")
        result.append({"severity": response.violence_result.severity, "type": "Violence"})
    return result

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

async def handle_moderation(message, user_message, is_private, flag, logs):
    """This function takes the messages that need moderating and handles the moderation"""
    try:
        response = responses.handle_responses(user_message, flag)
        handle_message = message.author.send(response) if is_private else await message.channel.send(response)
        await logs.send(f"{message.author} sent {message.content} and was moderated for {user_message}")
        await message.delete()
        print("This message has been removed")
    except Exception as e :
        print(f"was unable to return response {e}")

async def handle_command(message, user_message, is_private, flag):
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

    try:
        response = responses.handle_responses(user_message, flag)
        handle_message = message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(f"was un able to return response {e}")



def run_discord_bot():
    """This is the main function for running the bot"""
    intents = discord.Intents.all()
    token = os.environ["bot_token"]
    # print(TOKEN)
    client = discord.Client(intents=intents)
    logs = ""
    for server in client.guilds:
        for channel in server.channels:
            if str(channel.type) == 'text' and channel.name == "logs":
                logs = channel


    @client.event
    async def on_ready():
        print(f'{client.user} is ready!')

    @client.event
    async def on_message(message):

        # This stops the bot from replying to itself
        if message.author == client.user:
            return

        logs = ""
        for server in client.guilds:
            for channel in server.channels:
                if str(channel.type) == 'text' and channel.name == "logs":
                    logs = channel

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        moderation = azure_text_moderation(user_message)

        flag = False
        new_text = ""
        for res in moderation:
            new_text += f'{res["type"]}, '
        new_text = new_text[:-2]
        if len(moderation) > 0:
            flag = True
        print(f"{username} sent {user_message} in {channel}")

        if user_message[0] == "!":
            await handle_command(message, user_message, is_private=False, flag=flag)
        elif flag:
            await handle_moderation(message, new_text, is_private=False, flag=flag, logs=logs)
        else:
            await send_message(message, user_message, is_private=False, flag=flag)

    client.run(token)
