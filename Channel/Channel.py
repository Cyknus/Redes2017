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

    @staticmethod
    def server_up(client, my_port=Constants.CHAT_PORT):
        """ Levanta el servidor del cliente """
        api_server = MyApiServer(client, int(my_port))
        api_server_thread = Thread(target=api_server.server.serve_forever)
        api_server_thread.start()
        return api_server

    @staticmethod
    def connect_to(contact_ip = None, contact_port = Constants.CHAT_PORT):
        """
            Establece la conexión a un contacto
           @param <str> contact_ip: Si no se trabaja de manera local
                       representa la ip del contacto con el que se
                       establecerá la conexión
           @param <int> contact_port: De trabajar de manera local
                       representa el puerto de la instancia del contacto
        """

        if contact_ip:
            contact_server = ServerProxy('http://%s:%i'%(contact_ip, int(contact_port)), allow_none=True)
        else:
            contact_server = ServerProxy('http://localhost:%i'%int(contact_port), allow_none=True)

        return contact_server

    @staticmethod
    def send_text(text):
        """
            Se encarga de mandar un mensaje al contacto
            con el que se establece conexión.
        """
        pass
