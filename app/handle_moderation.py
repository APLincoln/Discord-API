import responses

async def handle_moderation(message, user_message, is_private, flag, logs, azure_response, gcp_response, moderation_responses):
    """This function takes the messages that need moderating and handles the moderation"""
    try:
        response = responses.handle_responses(user_message, flag)
        azure_message = ""
        for res in azure_response:
            azure_message += f"name: `{res['type']}` score: `{res['severity']}`\n"
        gcp_message = ""
        for res in gcp_response:
            gcp_message += f"name: `{res['name']}` score: `{res['confidence']}`\n"
        # handle_message = message.author.send(response) if is_private else await message.channel.send(response)
        await logs.send(f"{message.author} sent {message.content} and was moderated for {user_message}")
        await moderation_responses.send(f"Azure response: \n{azure_message}\n GCP Response: \n{gcp_message}")
        await message.delete()
        print("This message has been removed")
    except Exception as e :
        print(f"was unable to return response {e}")