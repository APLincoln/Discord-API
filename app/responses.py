
def handle_responses(message):
    l_message = message.lower()

    if l_message != '':
        return f"your message said `{message}`"
    if l_message == "test":
        return "well hello there"
    # here there will need to be some handling to handle the bad words
