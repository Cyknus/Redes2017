#! /usr/bin/env python3
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
from Constants.AuxiliarFunctions import *
from Constants.Constants import *
import threading

LOCALHOST = get_ip_address()

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
    def __init__(self, gui_parent, my_port=None):
        self.port = int(my_port) if my_port else CHAT_PORT
        self.ip = LOCALHOST
        # configurar el servidor
        self.chats_dictionary = {}
        wrapper = FunctionWrapper(gui_parent, self.chats_dictionary)
        self.server = SimpleXMLRPCServer((self.ip, self.port), requestHandler=RequestHandler)
        self.server.register_introspection_functions()
        self.server.register_multicall_functions()
        self.server.register_instance(wrapper)

    def run(self):
        print("[info] Raising server at " + str(self.ip) + "@" + str(self.port))
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()

    def remove_chat(self, username):
        self.chats_dictionary.pop(username)
        print("[debug] Active chats:")
        print(self.chats_dictionary)

class FunctionWrapper:
    """ **************************************************
    Constructor de la clase
    ************************************************** """
    def __init__(self, gui_parent, chats_dictionary):
        self.gui_parent = gui_parent
        self.chats_dictionary = chats_dictionary

    """**************************************************
    Metodo que sera llamado cuando un contacto quiera establecer
    conexion con este cliente
    **************************************************"""
    def new_chat_wrapper(self, contact_ip, contact_port, username):
        print("[info] New connection from: " + username + " ~ " + threading.current_thread().getName())
        if username not in self.chats_dictionary:
            self.gui_parent.current_screen.entry_connection(username, contact_ip, contact_port)
            self.chats_dictionary[username] = contact_ip
        return {"status": OK, "detailedInfo": "Connection ready"}

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
        print("[info] New message from " + contact_username)
        print(message)

        if contact_username in self.chats_dictionary:
            self.gui_parent.current_screen.entry_message(contact_username, contact_ip, text)
            return {"status": OK, "detailedInfo": "Got it"}
        else:
            return {"status": ERROR, "detailedInfo": "Connection closed"}


    """ **************************************************
    Procedimiento que ofrece nuestro servidor, este metodo sera llamado
    por el cliente con el que estamos hablando, debe de
    hacer lo necesario para regresar el texto
    ************************************************** """
    def echo(self, message):
        pass

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
