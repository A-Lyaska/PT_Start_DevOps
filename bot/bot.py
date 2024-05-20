import os
from dotenv import load_dotenv
import logging
import re
import paramiko
import psycopg2
from psycopg2 import Error
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram.error import BadRequest

load_dotenv()

TOKEN = os.getenv("TOKEN")

RM_HOST = os.getenv("RM_HOST")
RM_PORT = int(os.getenv("RM_PORT"))
RM_USER = os.getenv("RM_USER")
RM_PASSWORD = os.getenv("RM_PASSWORD")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_PORT = os.getenv("DB_PORT")

DB_REPL_USER = os.getenv("DB_REPL_USER")
DB_REPL_PASSWORD = os.getenv("DB_REPL_PASSWORD")
DB_REPL_HOST = os.getenv("DB_REPL_HOST")
DB_REPL_PORT = os.getenv("DB_REPL_PORT")

# Подключаем логирование
logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')


def helpCommand(update: Update, context):
    update.message.reply_text('Help!')


def findEmailsCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска email-адресов: ')

    return 'findEmails'
  
def findEmails(update: Update, context):
    user_input = update.message.text

    emailRegex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    emailList = emailRegex.findall(user_input)

    if not emailList:
        update.message.reply_text('Email-адрес(а) не найден(ы)')
        return

    emails = ''
    for i, email in enumerate(emailList, 1):
        emails += f'{i}. {email}\n'

    update.message.reply_text(emails)
    context.user_data['email_list'] = emailList
    update.message.reply_text('Желаете сохранить найденн(ые) email-адрес(а) в базу данных? (да/нет)')
    return 'confirm_save_emails'

def confirmSaveEmails(update: Update, context):
    user_response = update.message.text.lower()
    if user_response == 'да':
        email_list = context.user_data.get('email_list')
        if email_list is not None:
            save_emails_to_db(email_list)
            update.message.reply_text('Email-адрес(а) успешно сохранен(ы) в базе данных')
        else:
            update.message.reply_text('Список email-адресов пустой')
    elif user_response == 'нет':
        update.message.reply_text('Email-адрес(а) не будет(-ут) сохранены в базе данных')
    else:
        update.message.reply_text('Пожалуйста, введите "да" или "нет"')
        return 'confirm_save_emails'

    return ConversationHandler.END


def save_emails_to_db(email_list):
    connection = None
    try:
        connection = psycopg2.connect(user=DB_USER,
                                    password=DB_PASSWORD,
                                    host=DB_HOST,
                                    port=DB_PORT, 
                                    database=DB_DATABASE)
        cursor = connection.cursor()
        for email in email_list:
            cursor.execute("INSERT INTO emails(email) VALUES (%s);", (email,))
            connection.commit()
            logging.info("Email-адрес(а) успешно записан(ы) в базу данных")
    except (Exception, Error) as error:
        connection.rollback()
        logging.error("Ошибка при записи email-адресов в базу данных: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'find_phone_number'


def findPhoneNumbers (update: Update, context):
    user_input = update.message.text # Получаем текст, содержащий(или нет) номера телефонов

    phoneNumRegex = re.compile(r'(?:\+7|8)?[ \-]?\(?\d{3}\)?[ \-]?\d{3}[ \-]?\d{2}[ \-]?\d{2}') #

    phoneNumberList = phoneNumRegex.findall(user_input) # Ищем номера телефонов

    if not phoneNumberList: # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Телефонный(-ые) номер(а) не найден(ы)')
        return # Завершаем выполнение функции
    
    phoneNumbers = '' # Создаем строку, в которую будем записывать номера телефонов
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i+1}. {phoneNumberList[i]}\n' # Записываем очередной номер
        
    update.message.reply_text(phoneNumbers)
    context.user_data['phone_list'] = phoneNumberList
    update.message.reply_text('Желаете сохранить найденный(-ые) Телефонный(-ые) номер(а) в базу данных? (да/нет)')
    return 'confirm_save_phones'

def confirmSavePhones(update: Update, context):
    user_response = update.message.text.lower()
    if user_response == 'да':
        phone_list = context.user_data.get('phone_list')
        if phone_list is not None:
            save_phones_to_db(phone_list)
            update.message.reply_text('Телефонный(-ые) номер(а) успешно сохранен(ы) в базе данных')
        else:
            update.message.reply_text('Список Телефонных номеров пустой')
    elif user_response == 'нет':
        update.message.reply_text('Телефонный(-ые) номер(а) не будет(-ут) сохранен(ы) в базе данных')
    else:
        update.message.reply_text('Пожалуйста, введите "да" или "нет"')
        return 'confirm_save_phones'

    return ConversationHandler.END

def save_phones_to_db(phone_list):
    connection = None
    try:
        connection = psycopg2.connect(user=DB_USER,
                                    password=DB_PASSWORD,
                                    host=DB_HOST,
                                    port=DB_PORT, 
                                    database=DB_DATABASE)
        cursor = connection.cursor()
        for phone in phone_list:
            cursor.execute("INSERT INTO phones(phone) VALUES (%s);", (phone,))
            connection.commit()
            logging.info("Телефонный(-ые) номер(а) успешно записан(ы) в базу данных")
    except (Exception, Error) as error:
        connection.rollback()
        logging.error("Ошибка при записи Телефонных номеров в базу данных: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def echo(update: Update, context):
    update.message.reply_text(update.message.text)


def verifyPassword(update: Update, context):
    update.message.reply_text('Введите пароль для проверки сложности:')
    return 'verifyPassword'


def checkPasswordComplexity(password: str) -> bool:
    passwordRegex = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,}$')
    return bool(passwordRegex.match(password))


def handlePasswordVerification(update: Update, context):
    user_password = update.message.text

    if checkPasswordComplexity(user_password):
        update.message.reply_text('Пароль сложный')
    else:
        update.message.reply_text('Пароль простой')

    return ConversationHandler.END

def execute_ssh_command(hostname, port, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode()
    client.close()
    return output

def get_release(update: Update, context):
    command = "cat /etc/*release"
    result = execute_ssh_command(RM_HOST, RM_PORT, RM_USER, RM_PASSWORD, command)
    update.message.reply_text(result)

def get_uname(update: Update, context):
    command = "uname -a"
    result = execute_ssh_command(RM_HOST, RM_PORT, RM_USER, RM_PASSWORD, command)
    update.message.reply_text(result)

def get_uptime(update: Update, context):
    command = "uptime"
    result = execute_ssh_command(RM_HOST, RM_PORT, RM_USER, RM_PASSWORD, command)
    update.message.reply_text(result)

def get_df(update: Update, context):
    command = "df -h"
    result = execute_ssh_command(RM_HOST, RM_PORT, RM_USER, RM_PASSWORD, command)
    update.message.reply_text(result)

def get_free(update: Update, context):
    command = "free -h"
    result = execute_ssh_command(RM_HOST, RM_PORT, RM_USER, RM_PASSWORD, command)
    update.message.reply_text(result)

def get_mpstat(update: Update, context):
    command = "mpstat"
    result = execute_ssh_command(RM_HOST, RM_PORT, RM_USER, RM_PASSWORD, command)
    update.message.reply_text(result)

def get_w(update: Update, context):
    command = "w"
    result = execute_ssh_command(RM_HOST, RM_PORT, RM_USER, RM_PASSWORD, command)
    update.message.reply_text(result)

def get_auths(update: Update, context):
    command = "last -n 10"
    result = execute_ssh_command(RM_HOST, RM_PORT, RM_USER, RM_PASSWORD, command)
    update.message.reply_text(result)

def get_critical(update: Update, context):
    command = "journalctl -p crit -n 5"
    result = execute_ssh_command(RM_HOST, RM_PORT, RM_USER, RM_PASSWORD, command)
    update.message.reply_text(result)

def get_ps(update: Update, context):
    command = "ps aux | head"
    result = execute_ssh_command(RM_HOST, RM_PORT, RM_USER, RM_PASSWORD, command)
    update.message.reply_text(result)

def get_ss(update: Update, context):
    command = "ss -tunlp"
    result = execute_ssh_command(RM_HOST, RM_PORT, RM_USER, RM_PASSWORD, command)
    update.message.reply_text(result)

def get_apt_list(update: Update, context):
    package_name = ' '.join(context.args)
    if package_name:
        command = f"dpkg -l {package_name}"
    else:
        command = "dpkg -l"
    result = execute_ssh_command(RM_HOST, RM_PORT, RM_USER, RM_PASSWORD, command)
    
    max_message_length = 4096
    if len(result) > max_message_length:
        chunks = [result[i:i+max_message_length] for i in range(0, len(result), max_message_length)]
        for chunk in chunks:
            try:
                update.message.reply_text(chunk)
            except BadRequest as e:
                logger.error(f"Ошибка: {e}")
    else:
        update.message.reply_text(result)
    
def get_services(update: Update, context):
    command = "systemctl list-units --type=service | head -n 5"
    result = execute_ssh_command(RM_HOST, RM_PORT, RM_USER, RM_PASSWORD, command)
    update.message.reply_text(result)
    
def get_repl_logs(update: Update, context):
    command = "sudo docker logs db_repl_image --tail 10"
    result = execute_ssh_command(RM_HOST, RM_PORT, DB_USER, DB_PASSWORD, command)
    update.message.reply_text(result)    

def get_emails(update: Update, context):
    connection = None
    try:
        connection = psycopg2.connect(user=DB_USER,
                                    password=DB_PASSWORD,
                                    host=DB_HOST,
                                    port=DB_PORT, 
                                    database=DB_DATABASE)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM emails;")
        data = cursor.fetchall()
        answer = '\n'.join(str(row) for row in data)  # Преобразуем в строку каждую строку результата запроса
        update.message.reply_text(answer)  
        logging.info("Команда успешно выполнена")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
        
def get_phone_numbers(update: Update, context):
    connection = None
    try:
        connection = psycopg2.connect(user=DB_USER,
                                    password=DB_PASSWORD,
                                    host=DB_HOST,
                                    port=DB_PORT, 
                                    database=DB_DATABASE)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM phones;")
        data = cursor.fetchall()
        answer = '\n'.join(str(row) for row in data)  # Преобразуем в строку каждую строку результата запроса
        update.message.reply_text(answer)  
        logging.info("Команда успешно выполнена")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Обработчик диалога
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'find_phone_number': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
            'confirm_save_phones': [MessageHandler(Filters.text & ~Filters.command, confirmSavePhones)],
        },
        fallbacks=[]
    )
    
    convHandlerFindEmails = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailsCommand)],
        states={
            'findEmails': [MessageHandler(Filters.text & ~Filters.command, findEmails)],
            'confirm_save_emails': [MessageHandler(Filters.text & ~Filters.command, confirmSaveEmails)],
        },
        fallbacks=[]
    )

    
    convHandlerVerifyPassword = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verifyPassword)],
        states={'verifyPassword': [MessageHandler(Filters.text & ~Filters.command, handlePasswordVerification)]},
        fallbacks=[]
    )

        
	# Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmails)
    dp.add_handler(convHandlerVerifyPassword)
    dp.add_handler(CommandHandler("get_release", get_release))
    dp.add_handler(CommandHandler("get_uname", get_uname))
    dp.add_handler(CommandHandler("get_uptime", get_uptime))
    dp.add_handler(CommandHandler("get_df", get_df))
    dp.add_handler(CommandHandler("get_free", get_free))
    dp.add_handler(CommandHandler("get_mpstat", get_mpstat))
    dp.add_handler(CommandHandler("get_w", get_w))
    dp.add_handler(CommandHandler("get_auths", get_auths))
    dp.add_handler(CommandHandler("get_critical", get_critical))
    dp.add_handler(CommandHandler("get_ps", get_ps))
    dp.add_handler(CommandHandler("get_ss", get_ss))
    dp.add_handler(CommandHandler("get_apt_list", get_apt_list))
    dp.add_handler(CommandHandler("get_services", get_services))
    dp.add_handler(CommandHandler("get_repl_logs", get_repl_logs))
    dp.add_handler(CommandHandler("get_emails", get_emails))
    dp.add_handler(CommandHandler("get_phone_numbers", get_phone_numbers))
		
	# Регистрируем обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
		
	# Запускаем бота
    updater.start_polling()

	# Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
