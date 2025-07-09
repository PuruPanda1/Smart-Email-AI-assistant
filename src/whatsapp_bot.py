from twilio.rest import Client
from utils import format_message

def whatsapp_details(MAIL_ACTIONS, TWILIO_ACC_SID, TWILIO_AUTH_TOKEN):

    message = MAIL_ACTIONS[0]

    send_whatsapp_msg(message,TWILIO_ACC_SID ,TWILIO_AUTH_TOKEN)


def send_whatsapp_msg(msg, TWILIO_ACC_SID, TWILIO_AUTH_TOKEN):
    client = Client(TWILIO_ACC_SID, TWILIO_AUTH_TOKEN)

    msg = format_message(msg)

    try:
        message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=msg,
        to='whatsapp:+919073893382'
        )
        print(message.sid)
    except Exception as e:
        print(e)



