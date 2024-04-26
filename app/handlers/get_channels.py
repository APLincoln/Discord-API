"""This modules is used to return the required channels in a dict object"""

def channels(client):
    """This function will create a dict with the required channels within in it"""
    channels_dict = {}
    for server in client.guilds:
        for channel in server.channels:
            if str(channel.type):
                channels_dict.update({f"{channel.name}": channel})

    return channels_dict
