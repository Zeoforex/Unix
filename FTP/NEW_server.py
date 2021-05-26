import mimetypes
import os
import socket
import threading

''' Основная функция по работе с функционалом сервера '''


def process(req):
    global users
    user = users[0]
    homedir = '/home/dibirov/Python_Files/FTP/'
    ''' Проверка на соответствие пользователя и то что он есть у нас '''
    if (user in homedir):
        print("User exist!")
    else:
        print("User - ", user, " doesn't exist! Error!")

    ''' Отображение текущей директории '''
    if req.startswith('GET /pwd/'):
        with open('/home/dibirov/Python_Files/FTP/log.txt', 'w') as logs:
            logs.write('pwd ' + user)
        return os.getcwd()

    ''' Посмотреть содержимое папки(что внутри) '''
    elif req.startswith('GET /ls/'):
    with open('/home/dibirov/Python_Files/FTP/log.txt', 'w') as logs:
        logs.write('ls ' + user)
    str = "Directory name -> " + os.getcwd().split("/")[-1]
    return '; '.join(os.listdir())


''' Создать папку '''
elif req.startswith('GET /mkdir/'):
name = req.split()[1][7:]
try:
    os.mkdir(homedir + name)
    with open('/home/dibirov/Python_Files/FTP/log.txt', 'w') as logs:
        logs.write('mkdir ' + name + ' ' + user)
    return 'created'
except OSError:
    return 'error'

''' Удалить папку '''
elif req.startswith('GET /rmdir/'):
name = req.split()[1][7:]
try:
    resp = rmdir(homedir + name)
    if resp != 'error':
        with open('/home/dibirov/Python_Files/FTP/log.txt', 'w') as logs:
            logs.write('rmdir ' + name + ' ' + user)
    return resp
except OSError:
    return 'error'

''' Удалить файл '''
elif req.startswith('GET /delete/'):
name = req.split()[1][8:]
try:
    os.remove(homedir + name)
    with open('/home/dibirov/Python_Files/FTP/log.txt', 'w') as logs:
        logs.write('delete ' + name + ' ' + user)
    return 'deleted'
except OSError as e:
    print(e)
    return 'error'

''' Переименовать файл '''
elif req.startswith('GET /rename/'):
data = req.split()[1][7:]
prev = data.split('/')[1].replace('\\', '/')
now = data.split('/')[2].replace('\\', '/')
try:
    os.rename(homedir + prev, homedir + now)
    with open('//home/dibirov/Python_Files/FTP/log.txt', 'w') as logs:
        logs.write('rename ' + prev + ' ' + now + ' ' + user)
    return 'renamed'
except OSError as e:
    print(e)
    return 'error'

''' Получить файл с сервера'''
elif req.startswith('GET /receive/'):
data = req.split()[1][9:]
try:
    if data.endswith('.png') or data.endswith('.jpg') or data.endswith('.jpeg'):
        img = open(homedir + data, 'rb')
        b_img = img.read()
        return b_img
    else:
        with open(homedir + data, 'r') as file:
            with open('/home/grishinvv/Python_Files/FTP/server_log.txt', 'w') as logs:
                logs.write('receive ' + data + ' ' + user)
            return file.read()
except OSError as e:
    print(e)
    return 'error'

''' Остановка сервера '''
elif req.startswith('GET /stop/'):
return 'close connection'
else:
return 'bad request'

'''
Необходимо для многопользовательского взаимодействия с сервером (один сервер на одном потоке)
Грубо говоря чтобы было взимодействие не с одним человеком
Функция нужна для первоначального запуска всех остальных функций сервера. 
'''


def start(conn, addr):
    while True:
        request = conn.recv(1024).decode()
        print("Have received > ", request, " <")
        response = process(request)
        try:
            conn.send(response)
        except Exception as e:
            print(e)
            conn.send(response.encode())
        if request.startswith('GET /stop/'):
            conn.close()
            break


PORT = 8010
''' Наименование пользователя в системе Linux '''
users = ['Dibirov']
sock = socket.socket()
sock.bind(('', PORT))
sock.listen()

'''
Главный цикл, позволяющий серверу всегда быть включенным и ждать появления запроса от клиента
Он ждет пока придет соответствующий запрос от клиента и дожидается его
'''
while True:
    print("Listen to port -> ", PORT)
    conn, addr = sock.accept()
    print("Connected to this address -> ", addr)
    t = threading.Thread(target=start, args=(conn, addr))
    t.daemon = True
    t.start()