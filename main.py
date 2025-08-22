"""
import sys, subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "requests","telebot"])
url1 = "http://localhost:8001/"
request("открой новую вкладку")
"""
import pyttsx3,threading,requests,telebot,json,pyaudio,vosk
with open('config.json', 'r') as file:
    config = json.load(file)["config-main"]
from tts import TTS
from stt import STT
from gpt import Mistralai
tts = TTS()
stt = STT()
last_task = ""
name = False
def send_to_creator(e):
    bot = telebot.TeleBot(config)
    bot.send_message(chat_id=-1002099678922, text=e)
def request_task_to_analyse(speech_text):
    for name in config["active_names"]:
        if name in speech_text:
            speech_text.replace(name, "")
            break
    response = requests.post(url, json=data)
    if response.status_code == 200:
        res = response.json()
        threading.Thread(target=do_code, args=(res,)).start()
        threading.Thread(target=voice_syntize, args=(res, )).start()
    elif response.status_code == 404:
        pass
    else:
        send_to_creator(f"Ошибка в отправке запроса, код: {response.status_code} data: {data}")
    return

print("Все системы готовы")
try:
    while True:
        speech_text = stt.listen()
        if speech_text != last_task and speech_text != "":
            print(speech_text)
            threading.Thread(target=request_task_to_analyse, args=(speech_text,)).start()
        last_task = speech_text
except Exception as e:
    send_to_creator(f"Ошибка в исполнении: {e}")
