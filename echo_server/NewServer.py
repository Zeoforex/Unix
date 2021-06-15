#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

sock = socket.socket()

host=input("Введите адрес хоста: ")
port=int(input("Введите номер порта: "))

if not ((0<=port<65536) and isinstance(port, int)):
    print("Неправильный порт! Будет использоваться порт по умолчанию (9090)\n")
    port=9090

try:
    print("Соединение с сервером")
    sock.connect((host, int(port))) #127.0.0.1
except ConnectionResetError as error:
    print(error)
    print("Потеря связи с сервером")
    exit()

while True:
    # Отправка данных на сервер
    try:
        input_str = input('Ввод данных\n:>')
        if input_str.lower() == 'exit' or len(input_str) == 0:
            print("Разрыв соединения")
            sock.close()
            exit()
        else:
            try:
                sock.send(input_str.encode())
                print("Отправка данных серверу")
            except Exception as e:
                print(e)
                exit()
    except KeyboardInterrupt as keyint:
        print(keyint)
        print("Остановка программы")
        exit()

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

sock.close()
