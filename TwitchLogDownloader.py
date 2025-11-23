import requests
def get_text(channel,userText, year, month, day=""):
    link = f"https://logs.zonian.dev/channel/{channel}/{userText}{year}/{month}/{day}"
    print("Загружаю сообщения из")
    print(link)
    response = requests.get(link)
    text = response.text + "\n"
    return text

def add_log(fileName, text):
    with open(fileName, "a", encoding="utf-8") as f:
        f.write(text)

def programm():

    channel = "null"
    user = "null"

    year = 0
    month = 0

    startYear = "null"
    startMonth = "null"
    startDay = "null"
    endYear = "null"
    endMonth = "null"
    endDay = "null"

    channel = input("Twitch-канал:\n")
    user = input("Чаттер (оставьте пустым если нужен весь чат):\n")

    userText = f"user/{user}/"  # если логи на весь чат, то пустая строка

    if len(user) == 0:
        userText = ""

    periodInput = input("Период истории (пример: 2023-2 2025-11, для одного месяца: 2024-1,\nесли запрашивается весь чат, то надо ОБЯЗАТЕЛЬНО указывать еще и день: 2024-2-21):\n").split(" ")
    print("\n")

    startPeriod1 = list(map(int,periodInput[0].split("-")))
    startYear = startPeriod1[0]
    startMonth = startPeriod1[1]
    if len(startPeriod1) > 2:
        startDay = startPeriod1[2]
        startPeriod = f"{startYear}_{startMonth}_{startDay}"
    else:
        startPeriod = f"{startYear}_{startMonth}"

    if len(periodInput) > 1:
        endPeriod1 = list(map(int, periodInput[1].split("-")))
        endYear = endPeriod1[0]
        endMonth = endPeriod1[1]
        if len(endPeriod1) > 2:
            endDay = endPeriod1[2]
            endPeriod = f"-{endYear}_{endMonth}_{endDay}"
        else:
            endPeriod = f"-{endYear}_{endMonth}"
    else:
        endPeriod = ""

    period = f"{startPeriod}{endPeriod}"

    fileName = f"{channel}_{user}_{period}.txt"

    year = startYear
    month = startMonth
    if isinstance(startDay,int):
        day = startDay
    else:
        day = ""


    if len(endPeriod) > 0:
        while True:
            if isinstance(day,int):
                add_log(fileName, get_text(channel, userText, year, month, day))
                day += 1
                if day > 31:
                    month += 1
                if month > 12:
                    year += 1
                    month = 1
                    day = 1
                if (year > endYear) or (year == endYear and month > endMonth) or (year == endYear and month == endMonth and day > endDay):
                    break
            else:
                add_log(fileName, get_text(channel, userText, year, month))
                month += 1
                if month > 12:
                    year += 1
                    month = 1

                if (year > endYear) or (year == endYear and month > endMonth):
                    break
    else:
        if isinstance(day,int):

            add_log(fileName, get_text(channel, userText, startYear, startMonth, startDay))
        else:

            add_log(fileName, get_text(channel, userText, startYear, startMonth))

    if input('Введите "stop" для закрытия программы или закройте консоль:\n') == "stop":
        return
    else:
        start()


def start():
    try:
        programm()
    except Exception as e:
        print(str(e) + "\n\n")
        programm()

programm()



