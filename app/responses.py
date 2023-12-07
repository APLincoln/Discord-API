
def handle_responses(message, flag):
    l_message = message.lower()

    if l_message != '' and flag == False:
        return f"your message said `{message}`"
    if l_message != '' and flag:
        return f"this message has been moderated for `{message}`"
    if l_message == "test":
        return "well hello there"
    # here there will need to be some handling to handle the bad words
