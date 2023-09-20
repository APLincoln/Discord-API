import discord
import responses
from dotenv import load_dotenv
import os

load_dotenv()


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_responses(user_message)
        message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(f"was un able to return response {e}")


def run_discord_bot():
    intents = discord.Intents.all()
    token = os.environ["bot_token"]
    # print(TOKEN)
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is ready!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        print(message)
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} sent {user_message} in {channel}")

        if user_message[0] == "!":
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(token)
