"This module is used to moderate text using Azure"

import os
import discord
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions
from handlers import handle_moderation
from handlers import violations_database_handler as vdbh
from dotenv import load_dotenv
load_dotenv()

async def azure_text_moderation(message: discord.message,logs: discord.channel, hate_threshold: int,
                                selfharm_threshold: int, sexual_threshold:int, violence_threshold: int):
    """This function will take the message and send it to the azure content safety api
        This will return a value 0-7 the higher the number the more severe
    """
    endpoint = os.environ["endpoint"]
    key=os.environ["azure_token"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    flip_exclamation = str(message.content).replace("!", "i")
    filtered_text = ''.join(e for e in flip_exclamation if e.isalnum())

    # Check is made after filtering to make sure text isn't empty as request to Azure cannot be empty.
    if filtered_text == '':
        return []

    request= AnalyzeTextOptions(text=filtered_text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        # Any errors are caught and printed to console for logging, mitigating crash on failed request.
        print("Analyze image failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise
    result = handle_response(response=response, hate_threshold=hate_threshold, selfharm_threshold=selfharm_threshold,
                             sexual_threshold=sexual_threshold, violence_threshold=violence_threshold)
    await log_handler(azure_response=result, message=message,
                      logs=logs)
    return result


def handle_response(response, hate_threshold: int, selfharm_threshold: int,
                    sexual_threshold:int, violence_threshold: int):
    """Abstracting the handling of the response to enable testing of the function"""
    result = []
    for cat in response['categoriesAnalysis']:
        if cat['category'] == 'Hate' and cat['severity'] >= hate_threshold:
            result.append({"severity": cat['severity'], "type": "Hate"})
        if cat['category'] == 'SelfHarm' and cat['severity'] >= selfharm_threshold:
            result.append({"severity": cat['severity'], "type": "SelfHarm"})
        if cat['category'] == 'Sexual' and cat['severity'] >= sexual_threshold:
            result.append({"severity": cat['severity'], "type": "Sexual"})
        if cat['category'] == 'Violence' and cat['severity'] >= violence_threshold:
            result.append({"severity": cat['severity'], "type": "Violence"})
    return result

async def log_handler(azure_response, message: discord.Message,
                      logs: discord.channel):
    """This function will print required logs within logs channel"""
    mod_category_text = ""
    for res in azure_response:
        mod_category_text += f'{res["type"]}, '
    mod_category_text = mod_category_text[:-2]

    print(f"{message} was sent in {message.channel}")
    if len(azure_response) > 0:
        record = {"channel_name": message.channel.name, "violations": azure_response, "message": message.content, "date": message.created_at}
        vdbh.add_record(record)
        await handle_moderation.handle_moderation(message=message,
                                                  mod_category_text=mod_category_text,
                                                  logs=logs, azure_response=azure_response)
