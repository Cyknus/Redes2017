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
import logging

# Format responses
def build_response(func):
    def format_response(status, string_message):
        return {"status": status, "message": string_message}
    return format_response

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class MyApiServer:
    """
        Representa el servidor del usuario. A través de este
        el usuario recibe mensajes de sus contactos.

        @param gui_parent - elemento al que se notifican los mensajes
                            es una instancia de la GUI con métodos:
                                entry_message
                                entry_connection
                                entry_audio_call
        @param my_port - el puerto en el que se levanta el servidor
                         por defecto es: CHAT_PORT (5000)
    """
    def __init__(self, gui_parent, my_port=CHAT_PORT):
        self.port = int(my_port)
        self.ip = get_ip_address()
        self.chats_dictionary = {}
        # configurar el servidor
        wrapper = FunctionWrapper(gui_parent, self.chats_dictionary)
        self.server = SimpleXMLRPCServer((self.ip, self.port), requestHandler=RequestHandler)
        self.server.register_introspection_functions()
        self.server.register_instance(wrapper)
        # set logger '%(asctime)s %(name)-12s %(levelname)-8s %(message)s
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(name)-12s %(asctime)s :: %(message)s')
        handler.setFormatter(formatter)
        self.logger = logging.getLogger("MyApiServer")
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def run(self):
        self.logger.info("Local server running at %s@%d", self.ip, self.port)
        self.server.serve_forever()

    def stop(self):
        self.logger.debug("Shutting down server")
        self.server.shutdown()
        self.server.server_close()

    def remove_chat(self, username):
        self.logger.debug("Drop %s of chats_dictionary", username)
        self.logger.debug("Current active chats:\n%s", str(chats_dictionary))
        self.chats_dictionary.pop(username)

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
    def play_audio_wrapper(self,audio): # TODO decorator for entry message?
        self.gui_parent.current_screen.play_audio(audio.data)

    """ **************************************************
    Procedimiento que ofrece nuestro servidor, este metodo sera llamado
    por el cliente con el que estamos hablando, debe de
    hacer lo necesario para reproducir el video en la ventana adecuada
    ************************************************** """
    def play_video_wrapper(self,frame):
        pass

    def new_call_wrapper(self, type):
        txt_split = split_message_header(type)
        contact_username = txt_split[MESSAGE_USERNAME]
        contact_ip = txt_split[MESSAGE_IP]
        typo = txt_split[MESSAGE_TEXT]
        # TODO check if active
        if typo == AUDIO:
            print("New AudioCall from " + contact_username)
            self.gui_parent.current_screen.entry_audio_call(contact_username, contact_ip)
            return {"status": OK, "detailedInfo": "Stream ready"}
        return {"status": ERROR, "detailedInfo": "Unrecognized operation"}
