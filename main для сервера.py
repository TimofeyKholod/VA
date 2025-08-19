from flask import Flask, request, jsonify
import requests,g4f, telebot
from g4f.client import Client
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
g4f.debug.logging = False
g4f.check_version = False
client = Client()
messages = [{"role": "system", "content": "Ты - Джарвис, голосовой помощник, помогающий человеку. Давай ответы кратко и по существу."}]
config = requests.get("https://raw.githubusercontent.com/TimofeyKholod/VA/main/config_server.json").json()
question_words = config["question_words"]
app = Flask(__name__)
phrase_and_commands = requests.get(config["url_for_phrases"]).json()
phrases = list(phrase_and_commands.keys())
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(phrases)
callback_data = {"voice":[],
                 "code":""}
def send_to_creator(e):
    bot = telebot.TeleBot("6796190792:AAEngQeCe0z7XtwhyqCpB-1ADWgBOXx9VWo")
    bot.send_message(chat_id=-1002099678922, text=e)
def request_to_gpt(text):
    global messages
    messages += [{"role": "user", "content": f"Вопрос: {text}. Ответь на русском языке максимально кратко - только запрошенные данные. "}]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        web_search=False
    )
    messages += [{"role": "assistant", "content": response.choices[0].message.content}]
    return response.choices[0].message.content

def update_mes():
    if len(messages) >= 22:
        messages.pop(1)

def gen_text(text):
    callback_data["voice"] += [text]
@app.route('/analyse_command', methods=['GET','POST'])
def analyse_command():
    try:
        global messages
        data = request.get_json()
        speech_text = data["message"]
        task_vector = vectorizer.transform([speech_text])
        cosine_similarities = cosine_similarity(task_vector, X)
        most_similar_index = cosine_similarities.argmax()
        similar_phrase = phrases[most_similar_index]
        similarity_score = cosine_similarities[0][most_similar_index]
        function_name = phrase_and_commands[similar_phrase]
        if similarity_score >= 0.7 or data["have_name"]:
            url_of_function_code = f'https://raw.githubusercontent.com/TimofeyKholod/VA/main/commands/{function_name}.py'
            code_parts = requests.get(url_of_function_code).text.split('"""Client code part"""')
            exec(code_parts[0])
            callback_data["code"] = code_parts[1]
            messages += [{"role": "user", "content": f"Выполнена команда: {similar_phrase}"}]
            update_mes()
            return jsonify(callback_data), 200
        for question_word in question_words:
            if question_word in speech_text:
                gpt_ans = request_to_gpt(question_word)
                gen_text(gpt_ans)
                send_to_creator(f'Ответ gpt: \n {gpt_ans}')
                update_mes()
                return jsonify(callback_data), 200
    except Exception as e:
        send_to_creator(f"Ошибка на сервере:{e}")
    return "", 404
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001)
