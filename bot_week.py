import telebot

access_token = ''

# Создание бота с указанным токеном доступа
bot = telebot.TeleBot(access_token)

import requests


def get_page(group, week=''):  # получние страницы с расписанием по группе и неделе
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain='http://www.ifmo.ru/ru/schedule/0',
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


from bs4 import BeautifulSoup


def get_schedule(web_page, day=''):  # получение расписания данной группы на указанную неделю со страницы
    soup = BeautifulSoup(web_page, 'html5lib')

    dict_days = {'1': '1day', '2': '2day', '3': '3day', '4': '4day', '5': '5day',
                 '6': '6day'}
    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": dict_days.get(day)})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


import datetime
import time


@bot.message_handler(commands=['all'])
def get_day(message):
    try:
        _, week, group = message.text.split()
    except:
        bot.send_message(message.chat.id, 'Некорректный ввод данных. Введите команду, номер недели, группу',
                         parse_mode='HTML')
        return

    mas = ''
    dict = {'1': 'Понедельник', '2': 'Вторник', '3': 'Среда', '4': 'Четверг', '5': 'Пятница', '6': 'Суббота'}
    for day in range(1, 7):
        web_page = get_page(group, week)
        times_lst, locations_lst, lessons_lst = get_schedule(web_page, str(day))

        resp = ''
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        mas += '<b>{}</b>\n'.format(dict.get(str(day)))
        mas += '  '
        mas += resp

    bot.send_message(message.chat.id, mas, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)