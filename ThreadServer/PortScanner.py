#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import re
import threading
from datetime import datetime
import time
import os
from progress.bar import IncrementalBar 

'''
List of IPs
91.109.200.200 | Дата-центр в Москве
176.74.219.29 | Дата-центр в Чехии
4.2.2.2
77.88.21.11 | ya.ru
1.1.1.1 | Oracle
208.67.222.222 | OpenDNS
'''

portDict = {}
portList = []

numOfPorts = 65535

print(len(portList))

def validate_ip(s):
    a = s.split('.')
    if (len(a) != 4):
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if (i >= 256) or (i < 0):
            return False
    return True

def TryConnect(host, port):
    global portList
    sock = socket.socket()
    sock.settimeout(0.1)
    try:
        connect = sock.connect((host, port))
        string = 'Port : ' + str(port) + ' is open.'
        print("\n", string)
        portList.append(string)
        connect.close()
    except:
        pass


print("Запуск сервера")

while True:
    start = datetime.now()
    host=input("Введите адрес хоста: ").strip()

    if (host.lower() == "stop") or (host.lower() == "ыещз") or (host.lower() == "exit"):
        break

    print(">", host, "<")

    if (validate_ip(host) == True):
        Ping = os.system("ping -c 1 " + host)    
        if Ping == 0:
            print("Host is On Line!")

            portDict.update({host : "No ports online!"})
            
            bar = IncrementalBar('Scanning Ports', max = numOfPorts)

            for port in range(1, numOfPorts//2): #65536
                p1 = threading.Thread(target=TryConnect, args=[host, port])
                p1.start()
                bar.next()
                
                p2 = threading.Thread(target=TryConnect, args=[host, port*2])
                p2.start()

                bar.next()
                #time.sleep(1)
            
            bar.finish()
            
            if len(portList) != 0:
                portDict.update({host : portList})
            
            portList = []
            
        else:
            print(host, "is not avaluable ; (\n Try to enter IP again!\n", "*"*30)
    else:
        print("Wrong IP. Try to enter IP again!\n", "*"*30)
    
    ends = datetime.now()
    print('Time : {}'.format(ends-start))

print(portDict)
