#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading
import sys
import time

sock = socket.socket()
print("Запуск сервера")
host = socket.gethostbyname(socket.gethostname())
print('Server hosting on IP-> '+str(host))

port=int(input("Введите номер порта: "))
if not ((0<=port<65536) and isinstance(port, int)):
    print("Неправильный порт! Будет использоваться порт по умолчанию (9090)")
    port=9090

print("START TIME : " + str(time.ctime()))

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(('', int(port)))
sock.listen(3)
conn = []

client_message = ""

def Reciver():
    global client_message
    while 1:
        for i in range(len(conn)):
            try:
                data = conn[i].recv(1024).decode()
                if not data:
                    print("Нет данных")
                    break
                if len(data) == 0:
                    print("Пустое значение!")
                    break
                if data.lower() == 'sstop':
                    print("Отключение сервера!")
                    sys.exit()
                client_message = data
            except socket.error as e:
                if e.errno == 10053:
                    conn.pop(i)
                    print("Подключено пользователй:", len(conn))
                else:
                    raise
            except KeyboardInterrupt as keyint:
                print(keyint)
                print("Остановка программы")
                print("Потеря связи с сервером")
                exit()
            
def Sender():
    while 1:
        global conn
        #message = input()
        message = client_message
        if message:
            for i in range(len(conn)):
                conn[i].send(message.encode())

def Accepter():
    while 1:
        global conn
        conn_, addr = sock.accept()
        print("Подключение клиента")
        print('connected:', addr)
        print(conn_, " | ", sock.accept()[0])
        conn.append(sock.accept()[0])
        print("Подключено пользователей:", len(conn))


# init threads
t1 = threading.Thread(target=Reciver)
t2 = threading.Thread(target=Sender)
t3 = threading.Thread(target=Accepter)

# start threads
t1.start()
t2.start()
t3.start()
