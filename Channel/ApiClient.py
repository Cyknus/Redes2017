#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from Constants import *
from .Channel import Channel
from GUI.ikivy import MyLabel

import pyaudio

class MyApiClient:
    def  __init__(self):
        """ Constructor de la clase. """
        self.channel = Channel() # canal de comunicación

        # GUI
        self.display = None # Ligar la pantalla del chat

    def receive(self, message):
        """ Notifica en pantalla el mensaje recibido """
        # mostrar en pantalla el mensaje recibido
        msg = MyLabel(text=message, color=Constants.RGB_RECD)
        self.display.ids.layout.add_widget(msg)

    def play(self, audio):
        self.display.play(audio) # porquenosgustapasaralassiguientesfunciones
