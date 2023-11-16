import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('6797933164:AAH47RkvNb2X0LQ167KiLaZGcApcBTPGpzw')

@bot.message_handler(commands=['start', 'main', 'hello'])
def start_message(message):
    buttons = types.InlineKeyboardMarkup()
    buttons.add(types.InlineKeyboardButton('Посмотреть расписание', callback_data='show_schedule'))
    buttons.add(types.InlineKeyboardButton('Записаться на пару', callback_data='enroll'))
    buttons.add(types.InlineKeyboardButton('Кнопка для админов', callback_data='admin'))
    bot.send_message(message.chat.id, 'Привет! Это бот для записи на пары группы <b>ИНБО-01-21</b>.', parse_mode='html', reply_markup=buttons)

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Здесь будут правила записи.')

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'show_schedule':
        show_schedule(callback.message)
    elif callback.data == 'enroll':
        select_discipline(callback.message)
    elif r'd\w+;\w+; \w+ \w+ \w+' in callback.data:
        success_enroll(callback.message, callback.data[1:callback.data.find(';')], callback.data[callback.data.find(';') + 1:callback.data.find('; ')], callback.data[callback.data.find('; ') + 1:])
    elif callback.data.startswith('discipline - ') and ('; date - ' in callback.data):
        show_queue(callback.message, callback.data[callback.data.find('-') + 2:callback.data.find('; d')], callback.data[callback.data.find('; d') + 9:])
    elif callback.data.startswith('discipline - '):
        select_date(callback.message, callback.data[callback.data.find('-') + 2:])
    elif callback.data.startswith('confirm_student;'):
        confirm_student(callback.message, callback.data[callback.data.find('; di') + 15:callback.data.find('; da')], callback.data[callback.data.find('; da') + 9:])
    elif callback.data == 'admin':
        admin_password(callback.message)
    elif callback.data == 'show':
        show(callback.message)
    elif callback.data == 'delete':
        delete(callback.message)
    elif callback.data == 'insert':
        insert(callback.message)
    elif callback.data == 'show_users':
        show_users(callback.message)
    elif callback.data == 'show_disciplines':
        show_disciplines(callback.message)
    elif callback.data == 'show_date_with_disciplines':
        show_date_with_disciplines(callback.message)
    elif callback.data == 'cancel':
        start_message(callback.message)

def show_schedule(message):
    bot.send_message(message.chat.id, 'Расписание:')
    schedule = open('./schedule.png', 'rb')
    bot.send_document(message.chat.id, schedule)

def select_discipline(message):
    conn_db = sqlite3.connect('db.sql')
    cur_db = conn_db.cursor()
    cur_db.execute('SELECT title FROM discipline')
    disciplines = cur_db.fetchall()
    buttons = types.InlineKeyboardMarkup()
    for e in disciplines:
        buttons.add(types.InlineKeyboardButton(f'{e[0]}', callback_data=f'discipline - {e[0]}'))
    cur_db.close()
    conn_db.close()
    bot.send_message(message.chat.id, 'Выберите дисциплину:', reply_markup=buttons)

def select_date(message, discipline):
    conn_db = sqlite3.connect('db.sql')
    cur_db = conn_db.cursor()
    cur_db.execute(f'''SELECT date FROM date_and_discipline JOIN discipline ON date_and_discipline.discipline_id = discipline.id WHERE discipline.title = '{discipline}' ''')
    dates = cur_db.fetchall()
    buttons = types.InlineKeyboardMarkup()
    for e in dates:
        buttons.add(types.InlineKeyboardButton(f'{e[0]}', callback_data=f'discipline - {discipline}; date - {e[0]}'))
    cur_db.close()
    conn_db.close()
    bot.send_message(message.chat.id, f'Выбрана дисциплина {discipline}. Выберите дату.', reply_markup=buttons)

def show_queue(message, discipline, date):
    conn_db = sqlite3.connect('db.sql')
    cur_db = conn_db.cursor()
    cur_db.execute(f'''SELECT student.last_name, student.first_name, student.second_name FROM enroll JOIN student ON enroll.student_id = student.id JOIN date_and_discipline ON date_and_discipline.id = enroll.date_and_discipline_id JOIN discipline ON discipline.id = date_and_discipline.discipline_id WHERE date = '{date}' AND discipline.title = '{discipline}' ''')
    dates = cur_db.fetchall()
    users = ''
    for e in dates:
        users += f'\n{e[0]} {e[1]} {e[2]}'
    cur_db.close()
    conn_db.close()
    buttons = types.InlineKeyboardMarkup()
    buttons.add(types.InlineKeyboardButton('Записаться', callback_data=f'confirm_student; discipline - {discipline}; date - {date}'))
    buttons.add(types.InlineKeyboardButton('Отмена', callback_data='cancel'))
    bot.send_message(message.chat.id, f'Выбрана дисциплина {discipline}. Выбрана дата {date}. Список записавшихся:{users}', reply_markup=buttons)

def confirm_student(message, discipline, date):
    conn_db = sqlite3.connect('db.sql')
    cur_db = conn_db.cursor()
    cur_db.execute('SELECT * FROM student')
    student = cur_db.fetchall()
    buttons = types.InlineKeyboardMarkup()
    for e in student:
        buttons.add(types.InlineKeyboardButton(f'{e[1]} {e[2]} {e[3]}', callback_data=f'd{discipline};{date}; {e[1]}'))
    cur_db.close()
    conn_db.close()
    bot.send_message(message.chat.id, f'Выбрана дисциплина {discipline}. Выбрана дата {date}', reply_markup=buttons)

def success_enroll(message, discipline, date, student):
    conn_db = sqlite3.connect('db.sql')
    cur_db = conn_db.cursor()
    conn_db.commit()
    cur_db.close()
    conn_db.close()
    bot.send_message(message.chat.id, f'Запись успешно создана! {student} на {discipline} {date}.')

def admin_password(message):
    bot.send_message(message.chat.id, 'Введить пароль администратора:')

@bot.message_handler()
def info(message):
    if message.text == 'Qwerty':
        bot.send_message(message.chat.id, f'Добро пожаловать в систему изменения данных!')
        change_settings(message)
    else:
        bot.send_message(message.chat.id, 'Я Вас не понимаю.')

def change_settings(message):
    buttons = types.InlineKeyboardMarkup()
    buttons.add(types.InlineKeyboardButton('Посмотреть', callback_data='show'))
    buttons.add(types.InlineKeyboardButton('Удалить', callback_data='delete'))
    buttons.add(types.InlineKeyboardButton('Добавить', callback_data='insert'))
    bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=buttons)

def show(message):
    buttons = types.InlineKeyboardMarkup()
    buttons.add(types.InlineKeyboardButton('Посмотреть список группы', callback_data='show_users'))
    buttons.add(types.InlineKeyboardButton('Посмотреть список дисциплин', callback_data='show_disciplines'))
    buttons.add(types.InlineKeyboardButton('Посмотреть список дат по дисциплинам', callback_data='show_date_with_disciplines'))
    bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=buttons)

def delete(message):
    buttons = types.InlineKeyboardMarkup()
    buttons.add(types.InlineKeyboardButton('Удалить дисциплину', callback_data='delete_discipline'))
    bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=buttons)

def insert(message):
    buttons = types.InlineKeyboardMarkup()
    buttons.add(types.InlineKeyboardButton('Добавить дисциплину', callback_data='insert_discipline'))
    buttons.add(types.InlineKeyboardButton('Добавить дату', callback_data='insert_date'))
    bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=buttons)

def show_disciplines(message):
    conn_db = sqlite3.connect('db.sql')
    cur_db = conn_db.cursor()
    cur_db.execute('SELECT * FROM discipline')
    disciplines = cur_db.fetchall()
    disciplines_text = ''
    for e in disciplines:
        disciplines_text += f'\n{e[1]}'
    cur_db.close()
    conn_db.close()
    bot.send_message(message.chat.id, f'Дисциплины:{disciplines_text}')

def show_users(message):
    conn_db = sqlite3.connect('db.sql')
    cur_db = conn_db.cursor()
    cur_db.execute('SELECT * FROM student')
    disciplines = cur_db.fetchall()
    disciplines_text = ''
    for e in disciplines:
        disciplines_text += f'\n{e[1]} {e[2]} {e[3]}'
    cur_db.close()
    conn_db.close()
    bot.send_message(message.chat.id, f'Список группы:{disciplines_text}')

def show_date_with_disciplines(message):
    conn_db = sqlite3.connect('db.sql')
    cur_db = conn_db.cursor()
    cur_db.execute('SELECT discipline.title, date_and_discipline.date '
                   'FROM date_and_discipline '
                   'JOIN discipline '
                   'ON date_and_discipline.discipline_id = discipline.id '
                   'ORDER BY discipline.title')
    disciplines = cur_db.fetchall()
    disciplines_text = ''
    for e in disciplines:
        disciplines_text += f'\n{e[0]} {e[1]}'
    cur_db.close()
    conn_db.close()
    bot.send_message(message.chat.id, f'Список дат:{disciplines_text}')

bot.infinity_polling()