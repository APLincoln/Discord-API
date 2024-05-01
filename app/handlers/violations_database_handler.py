"""This module will act as the interface with an Azure SQL instance"""

import os, calendar
from datetime import datetime, date
import pyodbc, struct, paramiko
import discord
from azure import identity
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from dotenv import load_dotenv

load_dotenv()

def create_collection():
    """Initialise collection in DB"""
    client=MongoClient(os.environ["mongodb_connection_string"])
    db = client["ViolationsDB"]
    if "Violations" in db.list_collection_names():
        print("Collection ready to go!")
        return "collection already exists"
    else:
        print("Collection created and is now ready!")
        new_collection = db.create_collection("Violations")
    client.close()
    return "collection created!"

def add_record(record):
    """add record to DB"""
    client=MongoClient(os.environ["mongodb_connection_string"], server_api=ServerApi('1'))
    db = client["ViolationsDB"]
    collection = db["Violations"]
    insert=collection.insert_one(record)
    print(f"{insert.inserted_id} was inserted into table")
    client.close()
    return "done"

async def build_report(month:int, year:int, reports):
    """Takes a month and year to filter records from MongoDB and generate a report"""
    num_days = calendar.monthrange(year, month)[1]
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month, num_days)
    print(f"end: {end_date}")
    print(f"start: {start_date}")
    client=MongoClient(os.environ["mongodb_connection_string"], server_api=ServerApi('1'))
    db = client["ViolationsDB"]
    collection = db["Violations"]
    query = {
        "date": {
            "$gte": start_date,  # Greater than or equal to the start date
            "$lt": end_date      # Less than the end date
        }
    }
    results = collection.find(query)
    report = {}
    for document in results:
        print(document["violations"])
        for violation in document["violations"]:
            channel_name = document["channel_name"]
            violation_type = violation["type"]
            if channel_name not in report:
                report.update({f"{channel_name}": {f"{violation_type}": 1}})
            else:
                if violation_type not in report[f"{channel_name}"].keys():
                    report[f"{channel_name}"].update({f"{violation_type}": 1})
                else:
                    report[f"{channel_name}"][f"{violation_type}"] = report[f"{channel_name}"][f"{violation_type}"] + 1

    await handle_report(report=report, month=month, year=year, reports_channel=reports)
    client.close()
    print(report)

async def handle_report(report, month, year, reports_channel):
    """Takes report and sends embed in reports channel"""
    embed = discord.Embed(title = f"Report for {month}/{year}")
    for channel in report.keys():
        field_value = ""
        for violation in report[f"{channel}"].keys():
            violation_count = report[f"{channel}"][f"{violation}"]
            field_value += f"{violation}: {violation_count}\n"
        embed.add_field(name=f"{channel.title()}", value=field_value, inline=False)
    await reports_channel.send(embed=embed)
