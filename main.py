import mysql.connector
import telebot

bot = telebot.TeleBot('1598109413:AAGkAdYP7JJlWcJt5whGB0jJ0lQSujR1x6g')

#Подключение к БД
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="4658",
    port="3306",
    database="bot-telegram"
    )

cursor = db.cursor()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Старт')

@bot.message_handler(content_types=['text']) 
def send_message(message):
    if str.lower(message.text) == 'добавить студента':
        msg = bot.send_message(message.chat.id, 'Введите ФИО')
        bot.register_next_step_handler(msg, fullname_register)

    elif str.lower(message.text) == 'поиск':
        msg = bot.send_message(message.chat.id, 'Выберите категорию поиска')

    elif str.lower(message.text) == 'поиск по группе':
        msg = bot.send_message(message.chat.id, 'Введите группу')
        bot.register_next_step_handler(msg, search_by_group)

    #Ответ на произвольное сообщение
    else:
        bot.send_message(message.chat.id, 'oooops ...:(^_^):...')

#добавление студента
def fullname_register(message):
    try:
        fullname = message.text
        global last_name, first_name, middle_name
        last_name = fullname.split()[0]
        first_name = fullname.split()[1]
        middle_name = fullname.split()[2]
        msg = bot.send_message(message.chat.id, 'Введите группу')
        bot.register_next_step_handler(msg, group_register)
    except Exception as e:
        bot.send_message(message.chat.id, 'oooops...')

def group_register(message):
    global group
    group = message.text
    msg = bot.send_message(message.chat.id, 'Введите задолжность')
    bot.register_next_step_handler(msg, debt_register)

def debt_register(message):
    debt = message.text
    sql = "INSERT INTO users (first_name, middle_name, last_name, group_num, debt) VALUES (%s, %s, %s, %s, %s)"
    val = (first_name, middle_name, last_name, group, debt)
    cursor.execute(sql, val)
    db.commit()
    bot.send_message(message.chat.id, 'Готово!')
 
#Поиск по группе
def search_by_group(message):
    cursor.execute(f"SELECT COUNT(*) FROM users WHERE group_num='{message.text}'")
    num_col = cursor.fetchone()
    cursor.execute(f"SELECT * FROM users WHERE group_num='{message.text}'")
    for i in range(0, num_col[0]):
        result = cursor.fetchone()
        bot.send_message(message.chat.id, f"{i} ФИО: {result[1]} {result[2]} {result[3]}")
  
bot.polling()