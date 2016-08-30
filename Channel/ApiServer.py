#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from Constants import *
import pyaudio

class MyApiServer:
    def __init__(self, client):
        """
            Constructor de la clase.
            my_port : el puerto en el que escuchará el servidor
            client: el cliente al que notificará si hay nuevos mensajes
        """
        self.functions = FunctionWrapper(client) # idk

class FunctionWrapper:
    def __init__(self, client):
        """ Inicializa el marco de las funciones con el cliente dado"""
        self.client = client

    def sendMessage_wrapper(self, message):
        """
         Este método será llamado por el cliente con el que estamos hablando.
        """
        self.client.receive(message) # notificar el mensaje recibido

        return 1

    def listen(self, audio):
        self.client.stream.write(audio.data) # hey, te llaman

        return 1
