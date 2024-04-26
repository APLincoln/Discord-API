"""
This module is used to monitor the chat speed within a channel.
It will then handle the threshold being exceeded by placing the channel in a slow mode
"""

import datetime

async def check_for_spike(alert_channel, channel, threshold_time, threshold_count):
    """
    This function will look for chat spikes within the channel
    There is threshold set and if for a time, and if this is hit the channel
    will be put into slow mode.
    """

    time = datetime.datetime.now(datetime.UTC)
    time_with_delta = time - datetime.timedelta(seconds = threshold_time)
    # This flag will flipped to false if message within last count was sent before time threshold
    flag = True
    message_count = 0
    async for message in channel.history(limit=threshold_count):
        message_count += 1
        message_time = message.created_at
        if message_time < time_with_delta:
            flag = False

    if threshold_checker(flag=flag, current_delay=channel.slowmode_delay, message_count=message_count, threshold_count=threshold_count):
        await channel.edit(slowmode_delay=10)
        await alert_channel.send(f">>> Added slow down to {channel.name} due to a chat spike")

    return flag

def threshold_checker(flag:bool, current_delay:int, message_count:int, threshold_count:int):
    """checks if threshold met, pulled into seporate function for testing """
    return bool(flag and current_delay < 1 and message_count >= threshold_count)

