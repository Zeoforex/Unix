#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading
import sys

sock = socket.socket()

host = "127.0.0.1"
#host=input("Введите адрес хоста: ")

port=int(input("Введите номер порта: "))

if not ((0<=port<65536) and isinstance(port, int)):
    print("Неправильный порт! Будет использоваться порт по умолчанию (9090)\n")
    port=9090

try:
    print("Соединение с сервером")
    sock.connect((host, int(port)))
except ConnectionResetError as error:
    print(error)
    print("Потеря связи с сервером")
    exit()

def Reciver():
    while 1:
        # Прием данных от сервера
        try:
            data = sock.recv(1024).decode("utf8")
            if (len(data)==0):
                raise Exception("нет данных или потеря связи!")
            else:
                print("Прием данных от сервера")
                print(data + " | " + str(len(data)))
        except ConnectionResetError as error:
            print(error)
            print("Потеря связи с сервером")
            sock.close()
            exit()
        except Exception as ex:
            print(ex)
            sock.close()
            exit()

def Sender():
    while 1:
        # Отправка данных на сервер
        try: 
            message = input('Ввод данных\n:>')
            if message.lower() == "exit" or len(message) == 0:
                print("Разрыв соединения")            
                sock.close()
                sys.exit()
            else:
                try:
                    sock.send(message.encode())
                    print("Отправка данных серверу")
                except Exception as e:
                    print(e)
                    exit()
        except KeyboardInterrupt as keyint:
            print(keyint)
            print("Остановка программы")
            exit()

# init threads
t1 = threading.Thread(target=Reciver)
t2 = threading.Thread(target=Sender)

# start threads
t1.start()
t2.start()
