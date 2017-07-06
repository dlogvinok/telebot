from emoji import emojize
import os
import sqlite3

token = '385036836:AAEn4sCadUxTsb75c5ilQ3xIGJSA_yJNqWk'

events_name = ['Футбол', 'Хоккей', 'Баскетбол', 'Волейбол', 'Теннис']
events_name_live = ['Футбол-Live', 'Хоккей-Live', 'Баскетбол-Live', 'Волейбол-Live', 'Теннис-Live']

"""Параметры БД"""
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "telegram.db")

""" Сообщения для пользователей """
start_message = "Привет!\n" \
                "Я спортивный бот информатор.\n" \
                "Я помогу тебе узнать результаты спортивных событий "\
                "в прямом эфире.\n" \
                "Также, ты можешь воспользоваться другими полезными функциями " + emojize(":wink:", use_aliases=True) + '\n' \
                "Для справки введи команду /help.\n" \
                "Или вопсользуйся меню навигации."

help_message = "Описание в разработке"
back_to_menu = 'Выберите раздел'

"""Смайл"""
soccer = emojize(":soccer:", use_aliases=True)
basketball = emojize(':basketball:')
tennis = emojize(':tennis:')
volleyball = emojize(':baseball:')
hockey = emojize(':black_circle:')