import requests
import re
from dotenv import load_dotenv
import os
from constant import MAX_LENGTH, REASONING_LLM_MODEL, SUMMARY_LLM_MODEL, LLM_TEMPERATURE, BLOCKED_KEYWORDS, DEFAULT_SYSTEM_PROMPT
from imap_tools import MailBox, AND
from bs4 import BeautifulSoup
from utils import format_date
load_dotenv()


MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL")
TWILIO_ACC_SID = os.getenv("TWILIO_ACC_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

def retrieve_mails():
    with MailBox('imap.gmail.com').login(MAIL_USERNAME, MAIL_PASSWORD) as mailbox:
        mailbox.folder.set('Inbox')
        for msg in mailbox.fetch(AND(seen=False), mark_seen=False, limit=5, reverse=True):
            global MAIL_ACTIONS
            MAIL_ACTIONS = []
            msg_subject = msg.subject
            msg_from = msg.from_

            soup = BeautifulSoup(msg.html, "html.parser")
            msg_content = soup.get_text(separator="\n").strip()
        
            if len(msg_content) > MAX_LENGTH:
                msg_content = msg_content[:MAX_LENGTH]
        
            classify_mail(msg_from, msg_subject, msg_content)

def msg_llm(user_prompt, system_prompt=DEFAULT_SYSTEM_PROMPT, action="summary"):
    LLM_MODEL = SUMMARY_LLM_MODEL

    if action == "reasoning":
        LLM_MODEL = REASONING_LLM_MODEL

    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "temperature": LLM_TEMPERATURE
    }

    response = requests.post(f"{LM_STUDIO_URL}/chat/completions", headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()

    result = result["choices"][0]["message"]["content"].strip()

    return result

def classify_mail(mail_from, mail_subject, mail_content):
    user_prompt = f"""
        You are a smart email classifier.

        Your task is to classify an email as either `spam` or `important`.

        Definitions:
        - `spam`: Any email that is promotional, advertising, marketing, sales, or irrelevant.
        - `important`: Any email that is personal, work-related, or important communication.

        Examples:
        1)
        Header: "Limited Time Offer: Buy Now and Save 50%"
        Body: "Get our premium plan today and enjoy 50% off! Click here to buy now."
        => spam

        2)
        Header: "Meeting Reminder"
        Body: "Don't forget about the team meeting tomorrow at 10 AM."
        => important

        3)
        Header: "Exclusive Deal Just for You"
        Body: "Subscribe to our newsletter and get a free gift!"
        => spam

        4)
        Header: "Your application for leave has been approved"
        Body: "Your manager has approved your leave request for 15th July."
        => important

        Email to classify:
        Header: "{mail_subject}"
        Body: "{mail_content}"

        Respond with ONLY ONE WORD: `spam` or `important`.
    """

    system_prompt = """
        You are an email classifier. 
        You classify emails as `spam` or `important`. 
        Spam means any email that is promotional, advertising, marketing, sales, or irrelevant. 
        Important means personal, work-related, or important messages.
        Always respond with ONLY one word: `spam` or `important`. Do not explain.
    """
    
    combined_text = f"{mail_subject} {mail_content}".lower()
    
    if any(keyword in combined_text for keyword in BLOCKED_KEYWORDS):
        classification = "spam"
    else:
        classification = msg_llm(user_prompt, system_prompt, "reasoning").strip().split()[-1]

    print("Mail: ", mail_subject, " --> ", classification)

    if(classification.lower() == "important"):
        summarise_mail(mail_from, mail_subject, mail_content)
    else:
        print("Mailer: ", mail_from, " --> Spam")

def summarise_mail(mail_from, mail_subject, mail_content):
    user_prompt = f"""
        You are an assistant that summarises emails.
        Email details:
        Header: "{mail_subject}"
        Body: "{mail_content}"
    """

    system_prompt = (
        "Your task is to write a clear, concise summary of the email "
        "in **under 2 lines**. "
        "If the content is empty, generate the summary using only the subject. "
        "Do not add extra explanation. "
        "Return only the summary."
    )

    summary = msg_llm(user_prompt, system_prompt, "summary")

    next_steps(mail_from, mail_subject, summary)

def next_steps(mail_from, mail_subject, summary):
    user_prompt = f"""
    You are an assistant that generates next steps based on an email summary.
    Email Summary: "{summary}"
    """
    system_prompt = (
        "Your task is to suggest clear, actionable next steps based on the given email summary. "
        "If no action is needed, reply with 'No further actions required.' "
        "Provide maximum of 2 actions."
        "Return the result in this format:\n"
        "Next Steps: <your next steps or 'No further actions required'>"
    )

    actions = msg_llm(user_prompt, system_prompt, "reasoning")

    actions = re.sub(r"<think>.*?</think>", "", actions, flags=re.DOTALL).strip()
    actions = re.sub(r"next steps:", "", actions, flags=re.DOTALL).strip()


    MAIL_ACTIONS.append({
        "sender": mail_from,
        "subject": mail_subject,
        "summary": summary,
        "actions": actions,
        "reply": "To be implemented!"
    })
    
    return MAIL_ACTIONS
    # whatsapp_details(MAIL_ACTIONS, TWILIO_ACC_SID, TWILIO_AUTH_TOKEN)

def search_mail(keyword):
    message_list = []
    with MailBox('imap.gmail.com').login(MAIL_USERNAME, MAIL_PASSWORD) as mailbox:
        mailbox.folder.set('Inbox')
        for msg in mailbox.fetch(AND(subject=keyword), mark_seen=False, limit=5, reverse=True):
            subject = msg.subject
            sender = msg.from_
            date = msg.date

            message = (
                f"*Mail Sender:* {sender}\n"
                f"*On:* {format_date(date)}\n"
                f"*Subject:* {subject}\n\n"
            )

            message_list.append(message)

    response = f"Total Mail = {len(message_list)}\n"

    response += ''.join(message_list)
    
    return response