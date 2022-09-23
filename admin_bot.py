import telebot
from classBD import DB

print('Admin bot working')
token = ''
bot = telebot.TeleBot(token)

a = DB()



def list_id_users():
    list_id = []
    for id in a.get_admin_id():
        list_id.append(int(id[0]))
    return list_id


@bot.message_handler(commands=['start'])
def start_message(message):

    list_id = list_id_users()


    if message.chat.id in list_id:
        bot.send_message(message.chat.id, f'Приветсвуем вы авторизованы {message.chat.username}')
        mess = bot.send_message(message.chat.id, 'Введите имя пользователя')
        bot.register_next_step_handler(mess, func)
    elif message.chat.id not in list_id:
        mess = bot.send_message(message.chat.id, 'Введите пароль !')
        bot.register_next_step_handler(mess, password)


def password(message):
    if message.text == '123':
        a.insert_chat_id(message.chat.id)
        start_message(message)
    else:
        bot.send_message(message.chat.id, "Пароль не верный, сделайте рестарт бота и попробуйте еще раз")
        start_message(message)


def func(message):
    global name
    name = message.text
    if a.get_status(name):
        mark_up = telebot.types.ReplyKeyboardMarkup()
        item = telebot.types.KeyboardButton('Узнать статус')
        item2 = telebot.types.KeyboardButton('Изменить  статус')
        mark_up.add(item, item2)
        bot.send_message(message.chat.id, 'Нажмите на кнопку', reply_markup=mark_up)
    else:
        bot.send_message(message.chat.id, 'Пароль не верный попробуйте еще раз')
        start_message(message)


@bot.message_handler()
def get_status(message):
    if message.text == 'Узнать статус':
        bot.send_message(message.chat.id, a.get_status(name))
    if message.text == 'Изменить  статус':
        mark_up = telebot.types.ReplyKeyboardMarkup()
        item = telebot.types.KeyboardButton('0')
        item1 = telebot.types.KeyboardButton('1')
        item2 = telebot.types.KeyboardButton('2')
        item3 = telebot.types.KeyboardButton('3')
        mark_up.add(item, item1, item2, item3)
        mess = bot.send_message(message.chat.id, 'Нажмите кнопку для установки нового статуса ', reply_markup=mark_up)
        bot.register_next_step_handler(mess, func_3)


def func_3(message):
    a.admin_change_status(message.text, name)
    delete = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Статус изменен', reply_markup=delete)

    start_message(message)


bot.infinity_polling()
