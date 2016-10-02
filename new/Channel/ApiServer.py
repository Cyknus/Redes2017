#! /usr/bin/env python
# -*- coding: utf-8 -*-


#####################################################
# PURPOSE: Clase que permite mandar un mensaje al   #
#           contacto                                #
#                                                   #
# Vilchis Dominguez Miguel Alonso                   #
#       <mvilchis@ciencias.unam.mx>                 #
#                                                   #
# Notes:                                            #
#                                                   #
# Copyright   17-08-2015                            #
#                                                   #
# Distributed under terms of the MIT license.       #
#####################################################
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from AuxiliarFunctions import *
from Constants import *

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

"""**************************************************
Clase que genera un servidor de la biblioteca xmlrpc
con el cual el cliente expondrá los metodos que ofrece
@param gui_parent - Elemento gráfico por el que se
            muestran mensajes recibidos, etc.
@param my_port - Puerto donde se levanta el server
            si ninguno se especifica, se usa el default
**************************************************"""
class MyApiServer:
    def __init__(self, username, gui_parent, my_port = None):
        port = int(my_port) if my_port else CHAT_PORT
        ip = get_ip_address()
        header = get_message_header(username, ip)
        wrapper = FunctionWrapper(gui_parent, header)
        # configurar el servidor
        self.server = SimpleXMLRPCServer(ip, port)
        self.server.register_introspection_functions()
        self.server.register_multicall_functions()
        self.server.register_instance(wrapper)

    def run():
        self.server.serve_forever()

    def stop():
        self.server.shutdown()
        self.server.server_close()

class FunctionWrapper:
    """ **************************************************
    Constructor de la clase
    ************************************************** """
    def __init__(self, gui_parent, header):
        self.chats_dictionary = {} # conversaciones activas
        self.gui_parent = gui_parent
        self.header = header # header que se anexa a los mensajes

    """**************************************************
    Metodo que sera llamado cuando un contacto quiera establecer
    conexion con este cliente
    **************************************************"""
    def new_chat_wrapper(self, contact_ip, contact_port, username):
        connection = RequestChannel(self.header, contact_ip, contact_port)
        self.chats_dictionary[username] = {"ip": contact_ip, "connection": connection}
        # GUI

    """ **************************************************
    Procedimiento que ofrece nuestro servidor, este metodo sera llamado
    por el cliente con el que estamos hablando, debe de
    hacer lo necesario para mostrar el texto en nuestra pantalla.
    ************************************************** """
    def send_message_wrapper(self, message):
        message_split = split_message_header(message)
        contact_username =  message_split[MESSAGE_USERNAME]
        contact_ip = message_split[MESSAGE_IP]
        text = message_split[MESSAGE_TEXT]
        # GUI

    """ **************************************************
    Procedimiento que ofrece nuestro servidor, este metodo sera llamado
    por el cliente con el que estamos hablando, debe de
    hacer lo necesario para regresar el texto
    ************************************************** """
    def echo(self, message):
        message_split = split_message_header(message)
        contact_username =  message_split[MESSAGE_USERNAME]
        text = message_split[MESSAGE_TEXT]
        self.chats_dictionary[contact_username]["connection"].send_text(text)

    """ **************************************************
    Procedimiento que ofrece nuestro servidor, este metodo sera llamado
    por el cliente con el que estamos hablando, debe de
    hacer lo necesario para reproducir el audio
    ************************************************** """
    def play_audio_wrapper(self,audio):
        pass

    """ **************************************************
    Procedimiento que ofrece nuestro servidor, este metodo sera llamado
    por el cliente con el que estamos hablando, debe de
    hacer lo necesario para reproducir el video en la ventana adecuada
    ************************************************** """
    def play_video_wrapper(self,frame):
        pass
