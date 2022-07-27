from from_exel_to_sql import FromExelToSql
from classBD import DB
import telebot
from classProdbd import ProdBD


a = FromExelToSql()
b = DB()
c = ProdBD()

admin_token = '5481405794:AAGYtgp8-jZkaPc-57VZ3pvhqhJkOKjCq3s'
admin_bot = telebot.TeleBot(admin_token)

token = '5469974952:AAGIA_f9MTGCErdj0wcmrFylx1aY-7--sx8'
bot = telebot.TeleBot(token)


def get_art_from_cart(id):

    list_prod = []
    for elem in b.get_from_card(str(id)):
        list_prod.append(elem[0])
    return list_prod


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, f'Привет {message.from_user.username}')
        username = message.from_user.username
        user_id = message.chat.id
        b.add(user_id, username)
        mark_up = telebot.types.ReplyKeyboardMarkup()
        item = telebot.types.KeyboardButton('Получить информацию')
        mark_up.add(item)
        bot.send_message(message.chat.id, 'Выберите действие ', reply_markup=mark_up)
    elif message.text == '/help':
        text = "<a href='https://t.me/my11_admin_bot/'>admin</a>"
        bot.send_message(message.chat.id, text, parse_mode='HTML')


@bot.message_handler()
def func_1(message):
    if message.text == 'Получить информацию':
        mess = bot.send_message(message.chat.id, 'Введите артикул ')
        bot.register_next_step_handler(mess, func_2)
    elif message.text == 'Перейти в корзину':
        list_prod = get_art_from_cart(message.from_user.id)
        print(list_prod)
        if len(list_prod) == 0:
            bot.send_message(message.chat.id, 'Корзина пуста')
        else:

            mark_up = telebot.types.InlineKeyboardMarkup()
            but = telebot.types.InlineKeyboardButton('Удалить из корзины', callback_data='delete')
            mark_up.add(but)
            for art in list_prod:
                bot.send_message(message.chat.id, art, reply_markup=mark_up)
            mark_up2 = telebot.types.ReplyKeyboardMarkup()
            but_pay = telebot.types.KeyboardButton('Оплатить заказ')
            mark_up2.add(but_pay)
            bot.send_message(message.chat.id, 'Нажмите кнопку для оплаты заказа', reply_markup=mark_up2)
    elif message.text == 'Оплатить заказ':
        list_prod = get_art_from_cart(message.from_user.id)
        list_pay = []

        for art in list_prod:
            list_pay.append(telebot.types.LabeledPrice(art, int(str(c.get_prod_info(message.from_user.id, art)[0][4]) + '00')))

        bot.send_invoice(chat_id=message.from_user.id, title='name_prod', description='type_and_prod',
                         invoice_payload='price_window',
                         provider_token='401643678:TEST:c756da94-c0db-4d2a-ad37-c92447c2e841', currency='RUB',
                         start_parameter='', prices=list_pay)






def func_2(message):
    mark_up = telebot.types.InlineKeyboardMarkup()
    inline_btn = telebot.types.InlineKeyboardButton('Купить товар', callback_data='button')
    inline_btn_cart_add = telebot.types.InlineKeyboardButton('Добавить в корзину ', callback_data='add_to_cart')

    mark_up.add(inline_btn, inline_btn_cart_add)
    chat_id = message.chat.id
    global p
    p = c.get_prod_info(chat_id, message.text)[0]
    new_str = ''

    for elem in p:
        new_str += str(elem) + '\n'
    bot.send_message(message.chat.id, new_str, reply_markup=mark_up)


@bot.callback_query_handler(func=lambda call: True)
def func_3(call):
    global name_prod, price
    name_prod = p[0]
    type_and_prod = p[1] + ' ' + p[2]
    price = str(p[4]) + '00'

    if call.data == 'add_to_cart':
        mark_up = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_cart = telebot.types.KeyboardButton('Перейти в корзину ')
        item = telebot.types.KeyboardButton('Получить информацию')
        mark_up.add(btn_cart, item)
        user = call.from_user.id
        b.add_to_cart(user, name_prod)
        bot.send_message(call.from_user.id,
                         text='Ваш товар отправлен в корзину \nДля просмотра каталога нажмите Получить инфомацию',
                         reply_markup=mark_up)

    if call.data == 'button':

        bot.delete_message(call.from_user.id, call.message.message_id)
        bot.send_invoice(chat_id=call.from_user.id, title=name_prod, description=type_and_prod,
                         invoice_payload='price_window',
                         provider_token='401643678:TEST:c756da94-c0db-4d2a-ad37-c92447c2e841', currency='RUB',
                         start_parameter='', prices=[telebot.types.LabeledPrice(name_prod, int(price))])

    if call.data == "delete":
        b.delete_from_cart(str(call.from_user.id), call.message.text)
        bot.delete_message(call.from_user.id, call.message.message_id)


@bot.pre_checkout_query_handler(func=lambda call: True)
def process_pre_checkout_query(call):
    bot.answer_pre_checkout_query(call.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
def pay(message):
    if message.successful_payment.invoice_payload == 'price_window':
        bot.send_message(message.chat.id, 'Покупка прошла успешно')

        list_prod = get_art_from_cart(message.from_user.id)
        string = ''
        summ = 0
        for i in list_prod:
            string += i + ' ' + str(c.get_prod_info(message.chat.id, i)[0][4]) + '\n'
            summ += c.get_prod_info(message.chat.id, i)[0][4]
        string += 'Итого:' + str(summ)
        for elem in list_prod:
            print(elem)
            c.update_value_after_sale(elem)

        c.update_value_after_sale(p[0])

        for id in b.get_admin_id():
            admin_bot.send_message(chat_id=id[0], text=string)
        b.delete_after_pay(str(message.chat.id))

bot.infinity_polling()
'''1 удалить из базы после покупки 
2 правка сообщений админу
3 добавить title к invoice
4 потыкать по кнопкам (ошибки и исправить)'''