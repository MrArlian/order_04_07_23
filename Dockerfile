FROM python:3.9-alpine

RUN apk update && apk add --no-cache python3-dev build-base libffi-dev openssl-dev

WORKDIR /home/telegram_bot
COPY . /home/telegram_bot

RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]
