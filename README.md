# Smart Email AI Assistant System! 🚀

## How it works:<br>
 ✅ Retrieves the last 5 unread emails <br>
 ✅ Classifies them as important or spam<br>
 ✅ Summarises the content<br>
 ✅ Suggests “what actions to take”<br>
 ✅ If an email is important, it sends the details via WhatsApp<br>

## Tools used:<br>
🔧 Python + Docker for the backend<br>
🔧 LM Studio for running local LLMs<br>
🔧 DeepSeek R1 LLM for email classification and action suggestions<br>
🔧 Google Gemma 3 for generating summaries<br>
🔧 Twilio for WhatsApp messaging<br>

## How to use?
- Clone the repo
```
git clone https://github.com/PuruPanda1/Smart-Email-AI-assistant.git
```
- Setup .env file with following details
```
MAIL_PASSWORD = ""
MAIL_USERNAME = ""
LM_STUDIO_URL = ""
TWILIO_ACC_SID = ""
TWILIO_AUTH_TOKEN = ""
```
- Modify the CONSTANTS as per your needs in constant.py
```
MAX_LENGTH = 1000
REASONING_LLM_MODEL = "deepseek-r1-distill-qwen-1.5b"
SUMMARY_LLM_MODEL = "google/gemma-3-1b"
LLM_TEMPERATURE = 0.0

BLOCKED_KEYWORDS = [
        "stock market", "sensex", "nifty", "stocks",
        "equity", "shares", "market update", "trading"
    ]

```
- Build the docker container
```
docker build -t gmail_agent .
```
- Run the container
```
docker run -v $PWD:/app gmail_agent
```
- You will receive whatsapp for each important mail

### Note - Performance of the Agent depends on your GPU and PC power.

## Demo Video 

https://github.com/user-attachments/assets/84f366d0-5b06-4299-9839-02f26477ad79

## Whatsapp Screenshots

![whtsapp_screenshot](https://github.com/user-attachments/assets/9a2b812c-21f6-4ad7-bb09-37389c37846e)
