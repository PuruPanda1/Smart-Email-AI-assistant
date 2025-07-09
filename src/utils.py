from datetime import datetime

def format_date(date):
    formatted = date.strftime("%d %B %Y %H:%M")
    return formatted

def format_message(msg):
    sender = msg["sender"]
    subject = msg["subject"]
    summary = msg["summary"]
    actions = msg["actions"]

    message = (
        f"*Mail Sender:* {sender}\n"
        f"*Subject:* {subject}\n\n"
        f"*Summary:*\n{summary}\n\n"
        f"*Actions:*\n{actions}"
    )

    return message