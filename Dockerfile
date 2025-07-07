FROM python:3.11

WORKDIR /app
COPY main.py .
COPY requirements.txt .
COPY .env .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py" ]