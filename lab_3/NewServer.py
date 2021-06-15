#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time
import sys

sock = socket.socket()
log = open("ServerLog.txt", "a")
print("Запуск сервера")
log.write("Запуск сервера\n")

port=int(input("Введите номер порта: "))
if not ((0<=port<65536) and isinstance(port, int)):
    print("Неправильный порт! Будет использоваться порт по умолчанию (9090)")
    log.write('Неправильный порт! Будет использоваться порт по умолчанию 9090')
    port=9090

print("START TIME : " + str(time.ctime()))
log.write("START TIME : " + str(time.ctime()) + "\n")
sock.bind(('', int(port)))

while True:
    sock.listen(1)
    print("Начало прослушивание порта № " + str(port))
    log.write("Начало прослушивание порта № " + str(port))

    try:
        conn, addr = sock.accept()
        print("Подключение клиента")
        print('connected:', addr)
        log.write("Connected to " + addr[0] + ' ' + str(addr[1]) + "\n")
    except KeyboardInterrupt as keyint:
        print(keyint)
        print("Остановка программы")
        exit()


    while True:
        try:
            print("Прием данных от клиента")
            log.write("Прием данных от клиента\n")
            data = conn.recv(1024).decode("utf8")
            if not data:
                print("Нет данных")
                break
            if len(data) == 0:
                print("Пустое значение!")
                break
        except ConnectionResetError as error:
            print(error)
            print("Потеря связи с клиентом")
            exit()
        except KeyboardInterrupt as keyint:
            print(keyint)
            print("Остановка программы")
            print("Потеря связи с сервером")
            exit()


        print("Отправка данных клиенту")
        log.write("Отправка данных клиенту\n")
        log.write(str(data.upper().encode()) + "\n")
        conn.send(data.upper().encode())    
        print(str(sys.getsizeof(data)) + " bytes")    
        print("**************")
    
    
    print("Отключение клиента")
    log.write("Отключение клиента\n")
    conn.close()
log.close()
