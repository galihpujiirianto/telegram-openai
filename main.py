import os
import openai
import requests
from flask import Flask, request, Response

f = Flask(__name__)

model_engine = "text-davinci-003"
openai.api_key = os.environ.get("OPENAI_APIKEY")
TOKEN = os.environ.get("TOKEN")


def parsedata(value):
  chat_id = value["message"]["chat"]["id"]
  msg = value["message"]["text"]

  return chat_id, msg

def generate_text(prompt):
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message.strip()

def send_message(token, chat_id, msg):
  telegram_api = f"https://api.telegram.org/bot{token}/"
  params = {"chat_id": chat_id, "text": msg}

  r = requests.get(telegram_api + "sendMessage", params)
  return r

@f.route("/", methods=["GET", "POST"])
def main():
  if request.method == "POST":
    chat_id, msg = parsedata(request.get_json())
    if msg != "/start":
      ans = generate_text(msg)
    else:
      ans = "Halo kamu! Ini adalah bot yang menggunakan API OpenAI GPT.\n\nCredit: @graphiert"
    send_message(TOKEN, chat_id, ans)
    return Response("POST METHOD", 200)
  else:
    return Response("GET METHOD", 200)

if __name__ == "__main__":
  f.run(host='0.0.0.0', port='8080')

