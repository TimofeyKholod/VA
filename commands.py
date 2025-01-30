from vosk import Model, KaldiRecognizer
import time, requests, webbrowser, os, random,json,pyaudio
from datetime import datetime
from translate import Translator
from add_func import voice_text_el
minutes = 0
seconds = 0


with open("information.txt", "r", encoding="utf-8") as file:
    for line in file.readlines():
        if "Слова при выполнении команды:" in line:
            Dis = line.replace("Слова при выполнении команды:", "")
            Dis = Dis.split(', ')
def Dis_org():
    DIS = random.choice(Dis)
    voice_text_el(DIS)
def value_of_task(ver, task_name):
    max_timer_number = 0
    found_similar_task = False

    if len(ver) > 4:  # Проверка на длину
        if isinstance(ver[4], dict):
            for key in ver[4].keys():
                if key.startswith(task_name):
                    found_similar_task = True
                    timer_number = int(key[len(task_name):])
                    if timer_number > max_timer_number:
                        max_timer_number = timer_number
            if not found_similar_task:
                return 1
            return max_timer_number + 1
    return 1  # Если ver[4] не существует или не словарь, вернуть 1
#browser,getweather,task,cycle
def hello(ver):
    voice_text_el("Привет! Как я могу помочь вам сегодня?")
def open_new_tab(ver):
        #открой новую вкладку новая вкладка вкладку
        Dis_org()
        webbrowser.open(f'https://www.{ver[0]}.com/', new=1)
def open_sgo(ver):
    # 'открой сетевой город' in task or 'открой сг' in task or 'сетевой' in task:
        Dis_org()
        webbrowser.open('https://sgo.edu-74.ru/authorize/login', new=1)
def tab_with_search(ver):
        # 'открой вкладку' in task:
        Dis_org()
        ford = ver[2][:ver[2].find("у") + 2]# тут описано что task.find находит индекс первой у и находит все до первой у и плюс у с пробелом
        task = ver[2].replace(ford, '')# убирает открой вкладку вместе с пробелом
        webbrowser.open_new_tab(task)
def open_new_youtube_tab(ver):
        # "открой youtube" in task or "найди на youtube" in task:
        Dis_org()
        ford = ver[2][:ver[2].find("у") + 2]  # тут описано что task.find находит индекс первой у и находит все до первой у и плюс у с пробелом
        task = ver[2].replace(ford, '')  # убирает открой вкладку вместе с пробелом
        webbrowser.get().open("https://www.youtube.com/results?search_query=" + task)
def shutdown(ver):
    # "выключи компьютер" in task or "отключи компьютер" in task or "выруби компьютер" in task or "выруби все" in task or "отключи все" in task:
    Dis_org()
    voice_text_el('Отключаю питание')
    os.system('shutdown -s')
def time_hour(ver):
        # "который час" in task or "какой час" in task:
        current_datetime = datetime.now()
        hours = current_datetime.hour
        voice_text_el(f"сейчас {hours} часов")
def time_hour_minutes(ver):
        # "сколько время" in task or "время" in task:
        current_datetime = datetime.now()
        hours = current_datetime.hour
        minutes = current_datetime.minute
        voice_text_el(f"Время{hours} часов {minutes} минут")
def time_minutes(ver):
        # "сколько минут" in task or "минут" in task:

        current_datetime = datetime.now()
        minutes = current_datetime.minute
        voice_text_el(f"{minutes}  минут")
def time_day(ver):
        # "какое число" in task or "которое число" in task or "число" in task:

        current_datetime = datetime.now()
        day = current_datetime.day

        if day == 3:
           day = f"{day} тье число"
        else:
            day = f"{day} ое число"
        voice_text_el(day)
def time_day_of_week(ver):
        # "какой день недели" in task or "день недели" in task:
        current_datetime = datetime.now()
        day_of_week = current_datetime.isoweekday()
        text = ""
        if day_of_week == 1:
            text = "Понедельник"
        elif day_of_week == 2:
            text = "Вторник"
        elif day_of_week == 3:
            text = "Среда"
        elif day_of_week == 4:
            text = "Четверг"
        elif day_of_week == 5:
            text = "Пятница"
        elif day_of_week == 6:
            text = "Суббота"
        elif day_of_week == 7:
            text = "Воскресенье"

        voice_text_el(text)
def weather(ver):
    # "какая погода в" in task or "погода в" in task:
    task_name =f"weather{value_of_task(ver[4], 'weather')}"
    # Выполнение запроса к API
    print(ver[2])
    print(ver[1])
    response = requests.get('http://api.openweathermap.org/data/2.5/weather',
                            params={'q': ver[2], 'appid': 'cee13b782e0c4f0a65edecf47dd258b1', 'units': 'metric'},
                            timeout=20)
    # Проверка был ли запрос успешным
    ver[4][task_name] = "response"
    if response.status_code == 200:
        data = json.loads(response.text)
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        translator = Translator(to_lang="Russian")
        weather_description = translator.translate(weather_description)
        ver[4][task_name] = "complited"
        voice_text_el(f'Погода: {weather_description} Температура: {temperature} градусов Влажность: {humidity}% Скорость ветра {wind_speed} метров в секунду')
    else:
        voice_text_el("Произошла ошибка, отправлено вам")
        ver[4][task_name] = "error"
        print(response.text)
    ver[4].pop(task_name)
def set_timer(ver):
    # https://ru.stackoverflow.com/questions/1547543/c%D0%BF%D0%BE%D1%81%D0%BE%D0%B1-%D0%BF%D1%80%D0%B5%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D1%8C-%D1%87%D0%B8%D1%81%D0%BB%D0%BE%D0%B2%D1%8B%D0%B5-%D1%81%D0%BB%D0%BE%D0%B2%D0%B0-%D0%B2-%D1%86%D0%B5%D0%BB%D1%8B%D0%B5-%D1%87%D0%B8%D1%81%D0%BB%D0%B0-python
    timer = {
        "Часы": 0,
        "Минуты": 0,
        "Секунды": 0,
    }
    value = 0

    def add(count, value):
        return value + count

    def mul(count, value):
        return value * count

    startTokens = [

        [["один", "одна"], add(1, value)],
        [["два"], add(2, value)],
        [["три"], add(3, value)],
        [["четыре"], add(4, value)],
        [["пять"], add(5, value)],
        [["шесть"], add(6, value)],
        [["семь"], add(7, value)],
        [["восемь"], add(8, value)],
        [["девять"], add(9, value)],
        [["десять"], add(10, value)],

        [["десятков", "десяток", "десятка"], mul(10, value)],

        [["одиннадцать"], add(11, value)],
        [["двенадцать"], add(12, value)],
        [["тринадцать"], add(13, value)],
        [["четырнадцать"], add(14, value)],
        [["пятнадцать"], add(15, value)],
        [["шестнадцать"], add(16, value)],
        [["семнадцать"], add(17, value)],
        [["восемнадцать"], add(18, value)],
        [["девятнадцать"], add(19, value)],
        [["двадцать"], add(20, value)],
        [["тридцать"], add(30, value)],
        [["сорок"], add(40, value)],
        [["пятьдесят"], add(50, value)],
        [["шестьдесят"], add(60, value)],
        [["семьдесят"], add(70, value)],
        [["восемьдесят"], add(80, value)],
        [["девяносто"], add(90, value)],
        [["сто"], add(100, value)],

        [["сотен", "сотни"], mul(100, value)],

        [["двести"], add(200, value)],

        [["тысяч", "тысячи"], mul(1000, value)],
    ]
    tokens = ver[2].split(" ")
    value = 0
    for tokens_word in tokens:
        if "секунд" in str(tokens_word):
            timer["Секунды"] = value

            value = 0
            continue

        elif "минут" in str(tokens_word):
            timer["Минуты"] = value

            value = 0
            continue
        elif "час" in str(tokens_word):
            timer["Часы"] = value

            value = 0
            continue
        else:
            for tokens_start in startTokens:
                if str(tokens_word) in tokens_start[0]:
                    # print(tokens_start[1])

                    value += tokens_start[1]
    print(timer)
    while True:
        timer["Секунды"] -= 1
        if timer["Секунды"] == 0:
            if timer["Минуты"] == 0:
                if timer["Часы"] == 0:
                    print("время вышло")
                    break
                else:
                    timer["Часы"] -= 1
                    timer["Минуты"] = 59
                    timer["Секунды"] = 59
            else:
                timer["Минуты"] -= 1
                timer["Секунды"] = 59
        time.sleep(1)
        print(f"{timer['Часы']}:{timer['Минуты']}:{timer['Секунды']}")
#set_timer weather time_day_of_week time_day time_minutes time_hour_minutes time_hour shutdown open_new_youtube_tab tab_with_search open_sgo open_new_tab hello



