import telebot

access_token = '435454142:AAHVbxpy19BzX1ZxGyPFU_MYDBXyZRY-M18'

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

    dict_days = {'monday': '1day', 'tuesday': '2day', 'wednesday': '3day', 'thursday': '4day', 'friday': '5day',
                 'saturday': '6day'}
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


@bot.message_handler(commands=['DAY'])
def get_day(message):
    try:
        _, day, week, group = message.text.split()
    except:
        bot.send_message(message.chat.id,
                         'Некорректный ввод данных. Введите команду, день недели, номер недели и группу.',
                         parse_mode='HTML')
        return

    web_page = get_page(group, week)

    try:
        times_lst, locations_lst, lessons_lst = get_schedule(web_page, day)
    except:
        bot.send_message(message.chat.id,
                         'На указанный день занятий нет',
                         parse_mode='HTML')
        return None


    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)