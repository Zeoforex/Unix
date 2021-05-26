import logging
import os
import random
import socket
from datetime import datetime
from typing import Tuple

import magic

import utils
from valid import port_validation, check_port_open

'''
Возвращает текущую дату и время в формате Http Date(необходимую нам дату и время)
Пример: Date: day-name, day month year hour:minute:second GMT
'''

'''
Сама функция представлена внизу
'''
def get_date() -> str:
    now = datetime.now()
    stamp = mktime(now.timetuple())
    return format_date_time(stamp)


'''Класс запроса'''


class BrowserRequest:
    def __init__(self, data: bytes):
        lines = []
        # Чистим запрос
        for d in data.decode("utf8", "replace").split("\n"): # преобразуем в utf-8
            line = d.strip()
            if line:
                lines.append(line)

        self.method, self.path, self.http_version = lines.pop(0).split(" ")
        self.info = {k: v for k, v in (line.split(": ") for line in lines)}

    def __repr__(self) -> str:
        return f"<BrowserRequest {self.method} {self.path} {self.http_version}>"

    def __getattr__(self, name: str):
        try:
            return self.info["-".join([n.capitalize() for n in name.split("_")])]
        except IndexError:
            raise AttributeError(name)


'''Класс для сокетов'''


class LocaleSocket:

    # конструктор
    def __init__(self, host="", port=80, buffer_size=1024, max_queued_connections=5):
        self._connection = None
        self._socket = None
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.max_queued_connections = max_queued_connections

    def __repr__(self) -> str:
        status = "closed" if self._socket is None else "open"
        return f"<{status} ServerSocket {self.host}:{self.port}>"

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    #открытие
    def open(self):
        assert self._socket is None, "ServerSocket is closed"
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self._socket.bind((self.host, self.port))
        except Exception:
            self.close()
            raise
        else:
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def close(self):
        assert self._socket is not None, "Current ServerSocket was already closed"
        if self._connection:
            self._connection.close()
            self._connection = None
        self._socket.close()
        self._socket = None

    # слушаем и отправляем
    def listen(self) -> Tuple[BrowserRequest, str]:
        assert (self._socket is not None), "ServerSocket have to be in open mode"
        self._socket.listen(self.max_queued_connections)
        self._connection, address = self._socket.accept()
        data = self._connection.recv(self.buffer_size)
        return BrowserRequest(data), address[0]

    def send(self, data: bytes):
        assert self._socket is not None, "ServerSocket have to be open for response"
        self._connection.send(data)
        self._connection.close()


'''Класс сервера'''


class WebServer:
    '''Стандартные статусы ответа на запрос'''
    STATUSES = {
        200: "Ok",
        404: "File not found",
        403: "Forbidden"
    }

    '''
        port    -- порт, на котором разворачивается
        homedir -- домашняя директория
    '''

    # конструктор
    def __init__(self, config: dict, port: int = 80):
        self.socket = LocaleSocket(port=port, buffer_size=config["buffer_size"])
        self.homedir = os.path.abspath(config["homedir"])
    # функция запуска
    def start(self):
        """Запуск web-сервера"""
        self.socket.open()
        logger.info(f"Start Web-server on {self.socket.host}:{self.socket.port} | Homedir = {self.homedir}")
        while True:
            self.new_client_request()

    '''Остановка web-сервера'''

    def stop(self):
        self.socket.close()

    '''Роутер для ассоциации между путями и файлами'''

    def router(self, path: str) -> Tuple[bytes, int, str]:

        allowed_extensions = ["js", "html", "css", "png", "jpg"]

        router_dict = {
            "/": "index.html",
            "/index.html": "index.html",
            "/index": "index.html",
            "/test": "test.file",
            "/image": "first.jpeg"
        }

        if path in router_dict:

            '''Имя необходимого файла'''
            file_name = router_dict[path]

            if file_name.split(".")[1] in allowed_extensions:
                path_str = os.path.join(self.homedir, file_name)
                mime = magic.Magic(mime=True)
                mime_str = mime.from_file(path_str)
                with open(path_str, "rb") as f:
                    return f.read(), 200, mime_str

            else:
                with open(os.path.join(self.homedir, "403.html"), "rb") as f:
                    return f.read(), 403, "text/html"

        else:
            with open(os.path.join(self.homedir, "404.html"), "rb") as f:
                return f.read(), 404, "text/html"

    '''Обработка запроса клиента'''

    def new_client_request(self):

        cli_request, ip_addr = self.socket.listen()
        path = cli_request.path

        '''Информация о существовании файла'''

        body, status_code, mime = self.router(path)
        header = self.get_header(status_code, body, mime)
        self.socket.send(header.encode() + body)
        logger.info(
            f"{get_date()} -> {ip_addr}, {path} {status_code} - {cli_request.method} {cli_request.user_agent}")

    '''Получает заголовок для ответа сервера'''

    def get_header(self, status_code: int, body: str, mime: str):

        return "\n".join(
            [
                f"HTTP/1.1 {status_code} {self.STATUSES[status_code]}",
                f"Content-Type: {mime}",
                f"Date: {get_date()}",
                f"Content-length: {len(body)}",
                "Connection: close"
                "Server: MyServer" "\n\n",
            ]
        )


def main():
    default_port = 80
    port_input = input("Введите номер порта для сервера -> ")
    '''Проверка на занятость порта'''
    port_flag = port_validation(port_input, check_open=True)

    if not port_flag:

        port_input = default_port
        if not check_port_open(default_port):
            logger.info(
                f"Порт по умолчанию {default_port} уже занят! Подбираем рандомный порт.."
            )
            stop_flag = False
            current_port = None
            while not stop_flag:
                current_port = random.randint(49152, 65535)
                logger.info(f"Сгенерировали рандомный порт {current_port}")
                stop_flag = check_port_open(current_port)

            port_input = current_port
        logger.info(f"Выставили порт {port_input} по умолчанию")

    web_server = WebServer(config=config, port=int(port_input))
    web_server.start()
    web_server.stop()


if __name__ == "__main__":
    main()