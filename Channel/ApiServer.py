#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from xmlrpc.server import SimpleXMLRPCServer
from Constants import *

class MyApiServer:
    def __init__(self, my_port = Constants.CHAT_PORT, client_asoc = None):
        """
            Constructor de la clase.
            my_port : el puerto en el que escuchará el servidor
        """
        self.functions = FunctionWrapper(client_asoc)
        # configurar el servidor
        self.server = SimpleXMLRPCServer(("localhost", int(my_port)))
        self.server.register_introspection_functions()
        self.server.register_multicall_functions()
        self.server.register_instance(self.functions)

    def close(self): # TODO hay que ligar esto al cerrar la ventana
        self.server.shutdown()
        self.server.server_close()

class FunctionWrapper:
    def __init__(self, client):
        self.client = client

    def sendMessage_wrapper(self, message):
        """
         Este método será llamado por el cliente con el que estamos hablando.
        """
        self.client.receive(message)
        return 1 # códigos para estado de mensaje?
