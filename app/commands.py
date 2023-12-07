async def clear_command(number, channel):
    """Takes a number of messages to remove and a channel and will remove that many messages"""
    number = int(number)
    try:
        await channel.purge(limit=number)
    except Exception as e:
        print(f"error: {e}")
    return "complete"
