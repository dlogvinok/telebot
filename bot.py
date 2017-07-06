import constants
import telegram_db
import telebot
import sqlite3
from telebot import types
import parse
import re
import time

bot = telebot.TeleBot(constants.token)

"""Начальное меню"""

@bot.message_handler(commands=['start', 'help'])
def handler_start(message):
    """Обработка команд /start, /help
    Запись информации в БД
    """
    with sqlite3.connect(constants.db_path) as db:
        cur = db.cursor()
        telegram_db.add_user(message, db, cur)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Результаты онлайн', 'Ближайшие события']])

    if message.text == '/start':
        bot.send_message(message.chat.id, constants.start_message, reply_markup=keyboard)
    elif message.text == '/help':
        bot.send_message(message.chat.id, constants.help_message, reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Меню')
def back_to_menu(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Результаты онлайн', 'Ближайшие события']])
    bot.send_message(message.chat.id, constants.back_to_menu, reply_markup=keyboard)
    # bot.edit_message_reply_markup(message.chat.id, message.id,reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Результаты онлайн')
def handler_text(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in [
        '{}'.format('Футбол-Live', constants.soccer),
        '{}'.format('Хоккей-Live', constants.hockey),
        '{}'.format('Баскетбол-Live', constants.basketball),
        '{}'.format('Волейбол-Live', constants.volleyball),
        '{}'.format('Теннис-Live', constants.tennis),
        '{}'.format('Меню')]])
    bot.send_message(message.chat.id, 'Выберите вид спорта', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text in constants.events_name_live)
def handler_soccer(message):
    keyboard = types.InlineKeyboardMarkup()
    for i in parse.get_events(re.findall('[а-яА-Я]+', message.text)[0]):
        item = types.InlineKeyboardButton(text=i[0], callback_data='{}{}'.format(str(i[1]),'l'))
        keyboard.row(item)
    bot.send_message(message.chat.id, 'Выбирай', parse_mode='HTML', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: re.findall('\d+[a-zA-Z]{1}',call.data))
def inline_handler_event(call):
    if call.data[-1:] == 'l':
        champ = '<i>{}</i>'.format(parse.get_champ(call.data[:-1])[0])
        res = ''
        for i in parse.get_result(call.data[:-1]):
            res = res + str(i) + '\n'
        res = champ + '\n' + res
        keyboard = types.InlineKeyboardMarkup()
        item = types.InlineKeyboardButton(text='Назад', callback_data='back_to_events')
        keyboard.add(item)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=res,
                              parse_mode='HTML',
                              reply_markup=keyboard)


# @bot.callback_query_handler(func=lambda call: call.data == 'back_to_events')
# def inline_handler_back_to_event(call):

    # bot.edit_message_text(chat_id=call.mes,sage.chat.id,
    #                       message_id=call.message.message_id,
    #                       text=str(parse.get_champ(call.data)[0]))
    # for i in parse.get_result(call.data):
    #     keyboard = types.InlineKeyboardMarkup()
    #     item = types.InlineKeyboardButton(text='Подписаться на событие', callback_data='Y')
    #     keyboard.add(item)
    #     bot.send_message(call.message.chat.id, text = str(i), reply_markup=keyboard)


# @bot.callback_query_handler(func = lambda call: str(call.data) == 'Y')
# def inline_handler_p(call):
#     bot.edit_message_text(chat_id=call.message.chat.id,
#                           message_id=call.message.message_id,
#                           text='Ok')

# @bot.message_handler(func=lambda message: message.text == 'Хоккей-Live')
# def handler_hockey(message):
#     keyboard = types.InlineKeyboardMarkup()
#     m = parse.get_events('Хоккей')
#     if len(m) > 1:
#         for i in m:
#             item = types.InlineKeyboardButton(text=i[0], callback_data=str(i[1]), switch_inline_query='')
#             keyboard.row(item)
#         bot.send_message(message.chat.id, 'Выбирай', parse_mode='HTML', reply_markup=keyboard)
#     else:
#         bot.send_message(message.chat.id, 'В настоящий момент активных событий нет')

# @bot.message_handler(func=lambda message: message.text == 'Баскетбол-Live')
# def handler_soccer(message):
#     keyboard = types.InlineKeyboardMarkup()
#     for i in parse.get_events('Баскетбол'):
#         item = types.InlineKeyboardButton(text=i[0], callback_data=str(i[1]), switch_inline_query='')
#         keyboard.row(item)
#     bot.send_message(message.chat.id, 'Выберите событие', parse_mode='HTML', reply_markup=keyboard)


# @bot.message_handler(func = lambda message: 'Волейбол' in message.text)
# def handler_soccer(message):
#     keyboard = types.InlineKeyboardMarkup()
#     for i in parse.get_events('Волейбол'):
#         item = types.InlineKeyboardButton(text=i[0], callback_data=str(i[1]), switch_inline_query='')
#         keyboard.row(item)
#     bot.send_message(message.chat.id, 'Выбирай', parse_mode='HTML', reply_markup=keyboard)

@bot.message_handler(func=lambda message: 'Ближайшие события' == message.text)
def handler_text(message):
    with sqlite3.connect(constants.db_path) as db:
        cur = db.cursor()
        telegram_db.insert_line(db, cur)
        # print('Линия обновлена')

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in [
        '{}'.format('Футбол', constants.soccer),
        '{}'.format('Хоккей', constants.hockey),
        '{}'.format('Баскетбол', constants.basketball),
        '{}'.format('Волейбол', constants.volleyball),
        '{}'.format('Теннис', constants.tennis),
        '{}'.format('Меню')]])
    bot.send_message(message.chat.id, 'Выберите вид спорта', reply_markup=keyboard)

# noinspection PyGlobalUndefined
@bot.message_handler(func=lambda message: message.text in constants.events_name)
def handler_events(message, text=None, b=None):
    global txt

    if text is None:
        txt = message.text
    else:
        txt = text

    if b == True:
        msg_text = 'Событий нет.\nВыберите другое время события'
    else:
        msg_text = 'Выберите время события'

    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Ближайший час', callback_data='{}_hour_{}'.format(1, txt))
    keyboard.row(btn1)
    keyboard.add(*[types.InlineKeyboardButton(name, callback_data='{}_hour_{}'.format(name[0], txt))
                   for name in ['2 часа', '4 часа', '6 часов', '8 часов']])
    bot.send_message(message.chat.id, msg_text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: re.findall('\d+_', call.data))
def inline_handler_evetns_hour(call):
    with sqlite3.connect(constants.db_path) as db:
        cur = db.cursor()
        s = telegram_db.get_event_hour(db, cur, call.data[0], call.data)
        if len(s) > 0:
            keyboard = types.InlineKeyboardMarkup()
            for i in s:
                item = types.InlineKeyboardButton(text=i[0], callback_data=str(i[1]), switch_inline_query='')
                keyboard.row(item)
            keyboard.row(types.InlineKeyboardButton(text='<-Назад', callback_data='back_to_{}'.format(call.data)))
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Выберите событие',
                                  parse_mode='HTML',
                                  reply_markup=keyboard)
        else:
            #Если событий нет
            handler_events(call.message, call.data, False)

@bot.callback_query_handler(func=lambda call: re.findall('back_to_', call.data))
def handler_back_to_hour(call):
    """Сюда пойдем по кнопке Назад"""
    handler_events(call.message, call.data[7:], True)

# def update():
#     while True:
#         print('I works in same thread')
#         time.sleep(30)

if __name__ == '__main__':
    # import threading
    # Bot non-stop
    # t1 = threading.Event()
    # t1 = threading.Thread(target=update)
    # t2 = threading.Thread(target=bot.polling, args=(True,))
    # t1.start()
    # t2.start()
    # t1.join()
    # t2.join()
    bot.polling(none_stop=True)
