import telebot
from telebot import types
import keybord as keybord
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta
import sqlite3
import os

TOKEN = "514225550:AAEe19ZlPq80fXJwtM4vROm59SLnaKyGiU0"
bot = telebot.TeleBot(TOKEN)
conn = sqlite3.connect('user.db')
cursor = conn.cursor()

try:
    query = "CREATE TABLE \"main\" (\"user_id\" TEXT, \"teg_user\" TEXT)"
    cursor.execute(query)
except:
    pass


@bot.message_handler(commands=['start'])
def welcome(message):
    main_K = keybord.main_K()
    bot.send_message(message.chat.id, "Здравствуйте! Выберите акцию из избранных или введите новую!", parse_mode='html', reply_markup=main_K)



@bot.message_handler(content_types=['text'])
def treatment(message):
    if message.chat.type == 'private':
        if message.text == "Новая":
            teg_stock = bot.send_message(message.chat.id, 'Введите тэг нужной акции.', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(teg_stock, stocks)
        elif message.text == "Избранные":
            favorites(message)
        else:
            bot.send_message(message.chat.id, "К сожалению, я вас не понял, попробуйте еще раз",
                             parse_mode='html')


def stocks(message):

    def callback_worker(message):

        def now_price(message):
            msg = bot.send_message(message.from_user.id,
                                   text=f"Текущая цена акции {teg.upper()}: {result}\n")
            bot.register_next_step_handler(msg, callback_worker)

        def change_price(message):
            msg = bot.send_message(message.from_user.id,
                                   text=f"Цена акции {teg.upper()}, относительно прошлого торгового дня: {sum}({proc})")
            bot.register_next_step_handler(msg, callback_worker)

        def chart_for_mounth(message):
            data = yf.download(teg, datetime.date.today() - relativedelta(months=1), datetime.date.today())
            data['Adj Close'].plot()
            plt.title(f"Акция {teg.upper()}")
            plt.savefig(f'graphs_{message.from_user.id}.png')
            try:
                photo = open(f'graphs_{message.from_user.id}.png', "rb")
                os.remove(f'graphs_{message.from_user.id}.png')
            except:
                msg = bot.send_message(message.chat.id, 'Что то пошло не так. попробуйте еще раз')
                bot.register_next_step_handler(msg, callback_worker)
            msg = bot.send_photo(message.chat.id, photo)
            bot.register_next_step_handler(msg, callback_worker)

        def add_fav(message):
            with sqlite3.connect('user.db') as con:
                cursor = con.cursor()
                cursor.execute('SELECT teg_user FROM main WHERE user_id=={}'.format(message.from_user.id))
                tegs = cursor.fetchall()
                if len(tegs) > 5:
                    msg = bot.send_message(message.from_user.id,
                                           text="Количество избранных акций максимально!\n"
                                                "Для начала необходимо убрать уже добавленную!")
                else:
                    res = False
                    for i in tegs:
                        if str(i).find(teg) != -1:
                            res = True
                            break
                    if res:
                        msg = bot.send_message(message.from_user.id,
                                               text="Акция уже добавлена", reply_markup=keybord.stockIz_K())
                    else:
                        cursor.execute('INSERT INTO main (user_id, teg_user) VALUES (?, ?)', (message.from_user.id, teg))
                        msg = bot.send_message(message.from_user.id,
                                               text="Акция добавлена в избранное!", reply_markup=keybord.stockIz_K())
                bot.register_next_step_handler(msg, callback_worker)

        def delete_fav(message):
            with sqlite3.connect('user.db') as con:
                cursor = con.cursor()
                cursor.execute('DELETE FROM main WHERE user_id==? AND teg_user==?', (message.from_user.id, teg))
                msg = bot.send_message(message.from_user.id,
                                       text="Акция удалена из избранного!", reply_markup=keybord.stock_K())
                bot.register_next_step_handler(msg, callback_worker)

        if message.text == "Текущая цена":
            now_price(message)
        elif message.text == "Цена относительно вчерашнего дня":
            change_price(message)
        elif message.text == "График за последний месяц (только для иностранных акций)":
            chart_for_mounth(message)
        elif message.text == "Добавить в избранное":
            add_fav(message)
        elif message.text == "Удалить из избранного":
            delete_fav(message)
        elif message.text == "<-Назад":
            bot.send_message(message.from_user.id,
                             text="Вы вернулись в главное меню", reply_markup=keybord.main_K())
        else:
            msg = bot.send_message(message.chat.id, "К сожалению, я вас не понял, попробуйте еще раз",
                             parse_mode='html')
            bot.register_next_step_handler(msg, callback_worker)

    def clean_fav(message):
        with sqlite3.connect('user.db') as con:
            cursor = con.cursor()
            cursor.execute('DELETE FROM main WHERE user_id=={}'.format(message.from_user.id))
            bot.send_message(message.from_user.id,
                                   text="Акции удалены из избранного!",  reply_markup=keybord.main_K())

    if message.text == "<-Назад":
        bot.send_message(message.from_user.id,
                         text="Вы вернулись в главное меню", reply_markup=keybord.main_K())

    elif message.text == "Очистить список":
        clean_fav(message)
    else:
        teg = message.text.upper()
        with sqlite3.connect('user.db') as con:
            cursor = con.cursor()
            cursor.execute('SELECT teg_user FROM main WHERE user_id=={}'.format(message.from_user.id))
            tegs = cursor.fetchall()
            res = False
            for i in tegs:
                if str(i).find(teg) != -1:
                    res = True
                    break
            if res:
                stock_K = keybord.stockIz_K()
            else:
                stock_K = keybord.stock_K()
        try:
            page = requests.get(f"https://invest.yandex.ru/catalog/stock/{teg}/")
            soup = BeautifulSoup(page.content, 'html.parser')
            result = str(soup.find_all('div', class_="NoU3BzJNsF2eLlvl7PTcX"))
            result = result.replace('<div class="NoU3BzJNsF2eLlvl7PTcX">', "")
            result = result.replace('</div>', "").replace('[', "").replace(']', "")
            if len(result) > 12:
                result = result.rsplit(',', maxsplit=2)
                result = result[0].replace("\u202f", "")
            else:
                result = result.replace(' ', "")

            result2 = str(soup.find_all(class_="_2IV-LlapDqUTOMI29nwudZ"))
            result2 = result2.replace("</span>", "")
            result2 = result2.rsplit(">", maxsplit=5)
            sum = result2[1].rsplit("<")[0].replace("\u202f", "")
            proc = result2[3].rsplit("<")[0].replace("\u202f", "")

            msg = bot.send_message(message.from_user.id,
                                   text="Выбери необходимый пункт:", reply_markup=stock_K)
            bot.register_next_step_handler(msg, callback_worker)
        except:
            teg_stock = bot.send_message(message.chat.id, 'Что то пошло не так. Введите тэг еще раз',
                                         reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(teg_stock, stocks)


def favorites(message):
    favTeg_K = types.ReplyKeyboardMarkup()
    with sqlite3.connect('user.db') as con:
        cursor = con.cursor()
        cursor.execute('SELECT teg_user FROM main WHERE user_id=={}'.format(message.from_user.id))
        tegs = cursor.fetchall()
        if len(tegs) == 0:
            msg = bot.send_message(message.chat.id, "Список пуст. Вы можете добавить акции, через вкладку 'Найти'.", reply_markup=keybord.favoritFree_K())
            bot.register_next_step_handler(msg, stocks)
        else:
            for value in tegs:
                favTeg_K.add(types.KeyboardButton(value[0]))
            favTeg_K.add(types.KeyboardButton("Очистить список"))
            favTeg_K.add(types.KeyboardButton("<-Назад"))
            teg = bot.send_message(message.chat.id, "Выберите из списка интересующую акцию", reply_markup=favTeg_K)
            bot.register_next_step_handler(teg, stocks)


bot.polling(none_stop=True)
