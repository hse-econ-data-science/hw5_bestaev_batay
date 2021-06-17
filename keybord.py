from telebot import types
import telebot
import requests
from bs4 import BeautifulSoup

def main_K():
    main_K = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_K.row("Новая")
    main_K.row("Избранные")

    return main_K


def stock_K():
    stock_K = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Текущая цена')
    itembtn2 = types.KeyboardButton('Цена относительно вчерашнего дня')
    itembtn3 = types.KeyboardButton('График за последний месяц (только для иностранных акций)')
    itembtn4 = types.KeyboardButton('Добавить в избранное')
    itembtn5 = types.KeyboardButton('<-Назад')
    stock_K.add(itembtn1)
    stock_K.add(itembtn2)
    stock_K.add(itembtn3)
    stock_K.add(itembtn4)
    stock_K.add(itembtn5)


    return stock_K


def stockIz_K():
    stock_K = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Текущая цена')
    itembtn2 = types.KeyboardButton('Цена относительно вчерашнего дня')
    itembtn3 = types.KeyboardButton('График за последний месяц (только для иностранных акций)')
    itembtn4 = types.KeyboardButton('Удалить из избранного')
    itembtn5 = types.KeyboardButton('<-Назад')
    stock_K.add(itembtn1)
    stock_K.add(itembtn2)
    stock_K.add(itembtn3)
    stock_K.add(itembtn4)
    stock_K.add(itembtn5)

    return stock_K

def favoritFree_K():
    keybord = types.ReplyKeyboardMarkup()
    key = types.KeyboardButton('<-Назад')
    keybord.add(key)
    return keybord

# import yfinance as yf
#
# # Get the data for the stock AAPL
# data = yf.download('GAZP','2021-05-16','2021-06-16')
#
# # Import the plotting library
# import matplotlib.pyplot as plt
#
#
# # Plot the close price of the AAPL
# data['Adj Close'].plot()
# plt.show()

# page = requests.get("https://invest.yandex.ru/catalog/stock/aapl/")
# soup = BeautifulSoup(page.content, 'html.parser')
# result = str(soup.find_all(class_="_2IV-LlapDqUTOMI29nwudZ"))
# result = result.replace("</span>", "")
# result = result.rsplit(">", maxsplit=5)
# sum = result[1].rsplit("<")[0].replace("\u202f", "")
# proc = result[3].rsplit("<")[0].replace("\u202f", "")
# print(sum, proc)
# <div class="NoU3BzJNsF2eLlvl7PTcX">129,21  $</div>
