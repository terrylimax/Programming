import telebot

access_token = ''

# Создание бота с указанным токеном доступа
bot = telebot.TeleBot(access_token)

import requests


def get_page(group, week=''):
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


def get_schedule(web_page, day=''):
    soup = BeautifulSoup(web_page, 'html5lib')

    dict_days = {'1': '1day', '2': '2day', '3': '3day', '4': '4day', '5': '5day',
                 '6': '6day', '7': '1day'}
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


@bot.message_handler(commands=['nearest'])
def get_day(message):
    try:
        _, group = message.text.split()
    except:
        bot.send_message(message.chat.id, 'Некорректный ввод данных. Введите команду и номер группы.',
                         parse_mode='HTML')
        return

    now_day = datetime.datetime.now()  # получение сегодняшнего дня недели, времени
    day = str(now_day.isoweekday())
    now_time = str(now_day.strftime('%X'))

    web_page = get_page(group)
    new_day = day
    flag = 0
    while flag == 0:  # нахождение расписания ближайшего дня, где 100% есть пары
        try:
            times_lst, locations_lst, lessons_lst = get_schedule(web_page, new_day)
            flag = 1
        except:
            if new_day < '7':
                new_day = str(int(new_day) + 1)
            else:
                new_day = '1'

    if new_day != day:  # если это день не сегодняшний, то выводим просто его первую пару
        resp = '<b>{}</b>, {}, {}\n'.format(times_lst[0], locations_lst[0], lessons_lst[0])
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    else:  # иначе пытаемся понять какая пара из сегдняшнего дня ещё не началась
        times_list, locations_list, lessons_list = get_schedule(web_page, day)
        i = -1
        tuple = ()
        for time_lesson in times_list:
            try:
                now_time[0:2].rstrip(':')
                time_lesson[0:2].rstrip(':')
                now_time[3:5].rstrip(':')
                time_lesson[3:5].rstrip(':')
            except:
                pass
            i += 1
            if now_time[0:2] < time_lesson[0:2]:
                tuple = (times_list[i], locations_list[i], lessons_list[i])
                break
            elif now_time[0:2] == time_lesson[0:2]:
                if now_time[3:5] == time_lesson[3:5]:
                    tuple = (times_list[i], locations_list[i], lessons_list[i])
                    break
        if tuple:  # если такая нашлась, то выводим её
            times_list, locations_list, lessons_list = tuple
            resp = '<b>{}</b>, {}, {}\n'.format(times_list, locations_list, lessons_list)
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
        else:  # если все пары из сегодняшнего дня прошли, то выводим первую пару бляжайшего дня
            times_lst, locations_lst, lessons_lst = get_schedule(web_page, str(int(day) + 1))
            resp = '<b>{}</b>, {}, {}\n'.format(times_lst[0], locations_lst[0], lessons_lst[0])
            bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
