async def clear_command(number, channel):
    number = int(number)
    try:
        await channel.purge(limit=number)
    except Exception as e:
        print(f"error: {e}")
    return "complete"