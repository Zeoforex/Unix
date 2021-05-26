import socket

HOST = 'localhost'
PORT = 8090

'''
    *** Функции приложения ***

    0) Текущая директория - pwd
    1) Посмотреть содержимое папки - ls
    2) Создать папку - mkdir
    3) Удалить папку - rmdir
    4) Удалить файл - delete
    5) Переименовать файл - rename
    6) Копировать файл с клиента на сервер - (send file)
    7) Копировать файл с сервера на клиент - (get file)
    8) Выход (отключение клиента от сервера) - stop/disconnect/exit
'''

requests = ['GET /pwd/', 'GET /ls/', 'GET /mkdir/new', 'GET /rmdir/new', 'GET /delete/picture.png',
            'GET /rename/index.html/index.html', 'GET /receive/index.html', 'GET /stop/']
sock = socket.socket()
try:
    sock.connect((HOST, PORT))
except Exception as e:
    print(e)
for request in requests:
    sock.send(request.encode())
    try:
        response = sock.recv(1024).decode()
    except Exception as e:
        print(request)
        print(e)
    if response == 'error':
        print('Error in ' + request)
sock.close()