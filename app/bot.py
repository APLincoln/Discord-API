"""This is where the bot is run and events are triggered"""

import os
import discord
from discord.ext import commands
from handlers import azure_moderation, chat_speed, get_channels
from handlers import violations_database_handler as vdbh
from dotenv import load_dotenv

load_dotenv()

# Global Variables
threshold: int = 2
chat_spike_time_threshold: int = 60
chat_spike_message_threshold: int = 30

def get_guild_id(client):
    """This takes the client intialised and will return the guild id for the Discord server"""
    guild_id = ''
    for server in client.guilds:
        for channel in server.channels:
            guild_id = channel.guild.id
    return guild_id

def check_admin(interaction: discord.Integration):
    """Check if user has role admin"""
    if "admin" in [y.name.lower() for y in interaction.user.roles]:
        print("has admin")

def run_discord_bot(config):
    """This is the main function for running the bot"""
    intents = discord.Intents.all()
    token = os.environ["bot_token"]
    client = commands.Bot(command_prefix="/", intents=intents)


    @client.event
    async def on_ready():
        vdbh.create_collection()
        await client.tree.sync()
        print(f'{client.user} is ready!')

    @client.tree.command(name="clear", description = "This command will clear messages")
    @commands.has_permissions(manage_messages = True)
    async def _clear(ctx: discord.Interaction, amount: int= 10):
        role = discord.utils.get(ctx.guild.roles, name="tester")
        if role in ctx.user.roles:
            await ctx.response.defer(ephemeral=True)
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.response.send_message("you do not have the admin role", ephemeral=True)

    @client.tree.command(name="remove-slowdown",
                         description="This command will remove the slow mode")
    @commands.has_permissions(manage_messages = True)
    async def _remove_slow(ctx: discord.Interaction):
        role = discord.utils.get(ctx.guild.roles, name="tester")
        if role in ctx.user.roles:
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.response.send_message("slowdown removed", ephemeral=True)
        else:
            await ctx.response.send_message("you do not have the correct permission", ephemeral=True)

    @client.tree.command(name="build_report", description="build violation reports")
    async def _build_report(ctx:discord.Interaction, month:int = 0, year:int = 0):
        role = discord.utils.get(ctx.guild.roles, name="Admin")
        if role in ctx.user.roles:
            channel = discord.utils.get(ctx.guild.channels, name="reports")
            await vdbh.build_report(month = month, year = year, reports=channel)
            await ctx.response.send_message("please wait")
        else:
            await ctx.response.send_message("you do not have permisson to run this command")

    @client.event
    async def on_message(message):
        # This stops the bot from replying to itself
        if message.author == client.user:
            return

        channels = get_channels.channels(client)

        # This will check for a chat spike in the channel
        await chat_speed.check_for_spike(channel = message.channel,
                                         alert_channel=channels["alerts"],
                                         threshold_time = config["spike_time_threshold"],
                                         threshold_count = config["spike_count_threshold"])

        await azure_moderation.azure_text_moderation(hate_threshold=config["hate_threshold"],
                                                     selfharm_threshold=config["selfharm_threshold"],
                                                     sexual_threshold=config["sexual_threshold"],
                                                     violence_threshold=config["violence_threshold"],
                                                     message=message,
                                                     logs=channels["logs"])

    client.run(token)
