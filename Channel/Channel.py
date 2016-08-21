#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from xmlrpc.client import ServerProxy
from threading import Thread
from Constants import *
from .ApiServer import MyApiServer

class Channel:
    """
    Representa el canal de comunicación.
    Dado un puerto se levanta el servidor para el cliente y ofrece
    los métodos para conectarse con un contacto y enviar mensajes.
    """

    def  __init__(self, client, my_port = Constants.CHAT_PORT):
        """ Constructor de la clase. Establece el canal en el puerto dado """
        self.port = int(my_port)
        self.server = MyApiServer(self.port, client)
        api_server_thread = Thread(target=self.server.server.serve_forever)
        api_server_thread.start()

    def connect_to(self, contact_ip = None, contact_port = Constants.CHAT_PORT):
        """
            Establece la conexión a un contacto
           @param <str> contact_ip: Si no se trabaja de manera local
                       representa la ip del contacto con el que se
                       establecerá la conexión
           @param <int> contact_port: De trabajar de manera local
                       representa el puerto de la instancia del contacto
        """

        if contact_ip:
            self.contact_server = ServerProxy('http://%s:%i'%(contact_ip, contact_port), allow_none=True)
        else:
            self.contact_server = ServerProxy('http://localhost:%i'%contact_port, allow_none=True)

        # Establecer conexión bidireccional?
        # self.contact_server.ask("127.0.0.1", self.port)

    def send_text(self, text):
        """
            Se encarga de mandar un mensaje al contacto
            con el que se establece conexión.
        """
        self.contact_server.sendMessage_wrapper(text)
