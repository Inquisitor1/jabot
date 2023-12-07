#token: 6899730060:AAEcUHE7SJOkM7r87NiAupTJQ3038XqN0J0
import random

import telebot
from telebot import types

from tamagochik import create_frog
from tamagochik import Jaba

import time

bot = telebot.TeleBot('6899730060:AAEcUHE7SJOkM7r87NiAupTJQ3038XqN0J0')
global jaba
jaba = Jaba("")

@bot.message_handler(['start'])
def main(message):
    global user_id
    user_id = str(message.from_user.id)
    print(user_id)
    markup1 = types.InlineKeyboardMarkup()
    markup1.add(types.InlineKeyboardButton('Помощь', callback_data='help'))
    markup1.add(types.InlineKeyboardButton('Завести жабку', callback_data='new_frog'))
    bot.send_message(message.chat.id, f'<b>Привет, {message.from_user.first_name}!</b>\n\n* Для того, чтобы получить информацию об уходе за жабкой, выберите пункт <b>"Помощь"</b>\n* Чтобы завести жабку, выберите пункт <b>"Завести жабку"</b>', 'html', reply_markup=markup1)


def play(message):
            global jaba
            print(f'zhhh {jaba.get_name()}')
            print("name я работаю")
            print(user_id)
            if (jaba.update_stats() == False):
                is_dead(message)
            # file = open('Scripts/картинки/жаба_ счастливая.png', 'rb')
            # bot.send_photo(message.chat.id, file)
            if (jaba.get_name() == ""):
                bot.send_message(message.chat.id, "У вас нет лягушки, нажмите /start, чтобы начать")
            else:
                # bot.send_message(message.chat.id,
                # f'<b>Состояние лягушки:</b> \n\nГолод: {jaba.bellyful}\nСон: {jaba.sleep}\nГигиена: {jaba.hygiene}\nСчастье: {jaba.happiness}\n',
                # 'html')
                markup = types.ReplyKeyboardMarkup()
                btn = types.KeyboardButton('Информация о лягушке')
                markup.row(btn)
                btn1 = types.KeyboardButton('Покормить')
                btn2 = types.KeyboardButton('Помыть')
                markup.row(btn1, btn2)
                btn3 = types.KeyboardButton('Отправить спать')
                btn4 = types.KeyboardButton('Поиграть')
                markup.row(btn3, btn4)
                msg = bot.send_message(message.chat.id, 'Выберите: ', reply_markup=markup)
                #bot.register_next_step_handler(msg, on_click)

@bot.message_handler(content_types=['text'])
def ans(message):
    global jaba
    if jaba.get_name()=="":
        bot.send_message(message.chat.id, 'У вас  нет лягушки, выберите /start')
    else:
        if message.text == 'Информация о лягушке':
            bot.send_message(message.chat.id,
                             f'<b>Состояние лягушки:</b> \n\nГолод: {jaba.bellyful}\nСон: {jaba.sleep}\nГигиена: {jaba.hygiene}\nСчастье: {jaba.happiness}\n',
                             'html')
        elif message.text == 'Покормить':
            bot.send_message(message.chat.id, "Жабка поела", 'html')
            jaba.set_ate()
            if jaba.to_feed() == False:
                bot.send_message(message.chat.id, "Жабка лопнула", 'html')
                is_dead(message)
        elif message.text == 'Помыть':
            bot.send_message(message.chat.id, "Жабка помыта", 'html')
            jaba.set_washed()
            jaba.to_wash()
        elif message.text == 'Отправить спать':

            if(jaba.sleep < 100):
                jaba.go_sleep()
                bot.send_message(message.chat.id, 'Жаба спит')
                time.sleep(5)
                if (jaba.sleep < 100):
                    jaba.sleep += 20
                bot.send_message(message.chat.id, 'Жаба не спит')
                jaba.wake_up()
            else:
                bot.send_message(message.chat.id, 'Жаба не хочет спать')

        elif message.text == 'Поиграть':
            bot.send_message(message.chat.id, "Жабка поиграла", 'html')
            jaba.set_played()
            jaba.to_play()
        else:
            main(message)

def on_click(message):
    global jaba
    if message.text == 'Информация о лягушке':
        bot.send_message(message.chat.id,
                         f'<b>Состояние лягушки:</b> \n\nНасыщение: {jaba.bellyful}\nСон: {jaba.sleep}\nГигиена: {jaba.hygiene}\nСчастье: {jaba.happiness}\n',
                         'html')
        return True
    elif message.text == 'Покормить':
        jaba.set_ate()
        if jaba.to_feed() == False:
            is_dead(message)
        return
    elif message.text == 'Помыть':
        jaba.set_washed()
        jaba.to_wash()
    elif message.text == 'Отправить спать':
        jaba.set_slept()
        jaba.go_sleep()
    elif message.text == 'Поиграть':
        jaba.set_played()
        jaba.to_play()
    else:
        main(message)

@bot.callback_query_handler(func=lambda callback:True)
def callback_mes(callback):
    if callback.data == 'help':
        bot.send_message(callback.message.chat.id, '<b>Добро пожаловать в лучшую игру: симулятор ухода за жабкой!</b>\nОсновная задача - это обеспечить мирное и беззаботное существование земноводного. Не забывайте вовремя удовлетворять потребности вашего подопечного.', 'html')
    elif callback.data == 'new_frog':
        global jaba
        jaba = Jaba(user_id)
        jaba.from_file()
        print(f'1 {user_id}')
        if (user_id in jaba.jabas):
            jaba.set_name(user_id)
            bot.send_message(callback.message.chat.id, 'Ваша лягуха:')
        else:
            jaba.save_jaba(jaba)
            jaba.to_file()
            bot.send_message(callback.message.chat.id, f'Лягушка создана!')

@bot.message_handler(content_types=['photo', 'video', 'audio'])
def get_photo(message):
    i = random.randint(1,2)
    if i == 1:
        bot.reply_to(message, 'Лягушке понравилось! ☺')
    else:
        bot.reply_to(message, 'Лягушке не понравилось 👎')

def is_dead(message):
    bot.send_message(message.chat.id, "Жабка померла\nНаказание за вашу безответсвенность - это чувство вины на всю оставшуюся жизнь. Теперь живите с этим.\n<b>game over</b>", 'html')
    jaba.set_name('')
    main(message)

bot.polling(non_stop=True)