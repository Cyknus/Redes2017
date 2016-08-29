#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from xmlrpc.client import ServerProxy, Binary
from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread
from Constants import *
from .ApiServer import MyApiServer

class Channel:
    """
    Representa el canal de comunicación.
    Dado un puerto se levanta el servidor para el cliente y ofrece
    los métodos para conectarse con un contacto y enviar mensajes.
    """

    def __init__(self):
        """ Inicializa el canal con apuntadores None (hasta que se configuren)"""
        self.server = None # servidor asociado
        self.proxy = None # proxy al contacto

    def server_up(self, client, my_port=Constants.CHAT_PORT):
        """ Levanta el servidor del cliente
            Puede arrojar una excepción si el servidor no se puede lanzar.
        """
        api_server = MyApiServer(client) # servidor asociado a ese cliente
        # configuración de xmlrpc.. todo se hace aquí
        xmlrpc_server = SimpleXMLRPCServer(("localhost", int(my_port)))
        xmlrpc_server.register_introspection_functions()
        xmlrpc_server.register_multicall_functions()
        xmlrpc_server.register_instance(api_server.functions)
        # lanzar servidor
        api_server_thread = Thread(target=xmlrpc_server.serve_forever)
        api_server_thread.start()
        # guardar instancia para poder matar el hilo después
        self.server = xmlrpc_server

    def server_down(self):
        """ Detiene el hilo de ejecución del servidor del cliente"""
        self.server.shutdown()
        self.server.server_close()

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
            contact_server = ServerProxy('http://%s:%i'%(contact_ip, int(contact_port)), allow_none=True)
        else:
            contact_server = ServerProxy('http://localhost:%i'%int(contact_port), allow_none=True)

        self.proxy = contact_server


    def send_text(self, text):
        """
            Se encarga de mandar un mensaje al contacto
            con el que se establece conexión.
        """
        self.proxy.sendMessage_wrapper(text)

    def send_bytes(self, in_data):
        d = Binary(in_data)
        self.proxy.listen(d)
