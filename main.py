import logging
import re
import paramiko

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram.error import BadRequest


TOKEN = "6410163575:AAHyB8UhFfuiRsA3ftHbjYRFdNdSPFjcJQc"


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
        update.message.reply_text('Email-адреса не найдены')
        return

    emails = ''
    for i, email in enumerate(emailList, 1):
        emails += f'{i}. {email}\n'

    update.message.reply_text(emails)
    return ConversationHandler.END

def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'find_phone_number'


def findPhoneNumbers (update: Update, context):
    user_input = update.message.text # Получаем текст, содержащий(или нет) номера телефонов

    phoneNumRegex = re.compile(r'(?:\+7|8)?[ \-]?\(?\d{3}\)?[ \-]?\d{3}[ \-]?\d{2}[ \-]?\d{2}') #

    phoneNumberList = phoneNumRegex.findall(user_input) # Ищем номера телефонов

    if not phoneNumberList: # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Телефонные номера не найдены')
        return # Завершаем выполнение функции
    
    phoneNumbers = '' # Создаем строку, в которую будем записывать номера телефонов
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i+1}. {phoneNumberList[i]}\n' # Записываем очередной номер
        
    update.message.reply_text(phoneNumbers) # Отправляем сообщение пользователю
    return ConversationHandler.END # Завершаем работу обработчика диалога

def echo(update: Update, context):
    update.message.reply_text(update.message.text)


def verifyPassword(update: Update, context):
    update.message.reply_text('Введите пароль для проверки сложности:')
    return 'verifyPassword'


def checkPasswordComplexity(password: str) -> bool:
    # Регулярное выражение для проверки сложности пароля
    passwordRegex = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,}$')
    return bool(passwordRegex.match(password))


def handlePasswordVerification(update: Update, context):
    user_password = update.message.text  # Получаем введенный пользователем пароль

    if checkPasswordComplexity(user_password):
        update.message.reply_text('Пароль сложный')
    else:
        update.message.reply_text('Пароль простой')

    return ConversationHandler.END

def execute_ssh_command(hostname, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, username=username, password=password)
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode()
    client.close()
    return output

def get_release(update: Update, context):
    hostname = "192.168.19.164"
    username = "a_lyaska"
    password = "Nik2104"
    command = "cat /etc/*release"

    result = execute_ssh_command(hostname, username, password, command)
    update.message.reply_text(result)

def get_uname(update: Update, context):
    hostname = "192.168.19.164"
    username = "a_lyaska"
    password = "Nik2104"
    command = "uname -a"

    result = execute_ssh_command(hostname, username, password, command)
    update.message.reply_text(result)

def get_uptime(update: Update, context):
    hostname = "192.168.19.164"
    username = "a_lyaska"
    password = "Nik2104"
    command = "uptime"

    result = execute_ssh_command(hostname, username, password, command)
    update.message.reply_text(result)

def get_df(update: Update, context):
    hostname = "192.168.19.164"
    username = "a_lyaska"
    password = "Nik2104"
    command = "df -h"

    result = execute_ssh_command(hostname, username, password, command)
    update.message.reply_text(result)

def get_free(update: Update, context):
    hostname = "192.168.19.164"
    username = "a_lyaska"
    password = "Nik2104"
    command = "free -h"

    result = execute_ssh_command(hostname, username, password, command)
    update.message.reply_text(result)

def get_mpstat(update: Update, context):
    hostname = "192.168.19.164"
    username = "a_lyaska"
    password = "Nik2104"
    command = "mpstat"

    result = execute_ssh_command(hostname, username, password, command)
    update.message.reply_text(result)

def get_w(update: Update, context):
    hostname = "192.168.19.164"
    username = "a_lyaska"
    password = "Nik2104"
    command = "w"

    result = execute_ssh_command(hostname, username, password, command)
    update.message.reply_text(result)

def get_auths(update: Update, context):
    hostname = "192.168.19.164"
    username = "a_lyaska"
    password = "Nik2104"
    command = "last -n 10"

    result = execute_ssh_command(hostname, username, password, command)
    update.message.reply_text(result)

def get_critical(update: Update, context):
    hostname = "192.168.19.164"
    username = "a_lyaska"
    password = "Nik2104"
    command = "journalctl -p crit -n 5"

    result = execute_ssh_command(hostname, username, password, command)
    update.message.reply_text(result)

def get_ps(update: Update, context):
    hostname = "192.168.19.164"
    username = "a_lyaska"
    password = "Nik2104"
    command = "ps aux | head"

    result = execute_ssh_command(hostname, username, password, command)
    update.message.reply_text(result)

def get_ss(update: Update, context):
    hostname = "192.168.19.164"
    username = "a_lyaska"
    password = "Nik2104"
    command = "ss -tunlp"

    result = execute_ssh_command(hostname, username, password, command)
    update.message.reply_text(result)

def get_apt_list(update: Update, context):
    hostname = "192.168.19.164"
    username = "a_lyaska"
    password = "Nik2104"
    package_name = ' '.join(context.args)
    if package_name:
        command = f"dpkg -l {package_name}"
    else:
        command = "dpkg -l"

    result = execute_ssh_command(hostname, username, password, command)
    
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
    hostname = "192.168.19.164"
    username = "a_lyaska"
    password = "Nik2104"
    command = "systemctl list-units --type=service | head -n 5"

    result = execute_ssh_command(hostname, username, password, command)
    update.message.reply_text(result)
    
def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Обработчик диалога
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'find_phone_number': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
        },
        fallbacks=[]
    )
    
    convHandlerFindEmails = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailsCommand)],
        states={
            'find_email': [MessageHandler(Filters.text & ~Filters.command, findEmails)],
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
    
		
	# Регистрируем обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
		
	# Запускаем бота
    updater.start_polling()

	# Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
