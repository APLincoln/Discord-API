"""This modules is used to return the required channels in a dict object"""

def channels(client):
    """This function will create a dict with the required channels within in it"""
    channels_dict = {}
    for server in client.guilds:
        for channel in server.channels:
            if str(channel.type) == 'text' and channel.name == "logs":
                channels_dict.update({"logs": channel})
            elif str(channel.type) == 'text' and channel.name == "moderation-responses":
                channels_dict.update({"moderation-responses": channel})
            elif str(channel.type) == 'text' and channel.name == "alerts":
                channels_dict.update({"alerts": channel})
    return channels_dict
