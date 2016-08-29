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
        self.display = None # donde se agregarán los mensajes

    def receive(self, message):
        """ Notifica en pantalla el mensaje recibido """
        # mostrar en pantalla el mensaje recibido
        msg = MyLabel(text=message, color=Constants.RGB_RECD)
        self.display.add_widget(msg)

    def play(self, audio):
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(Constants.WIDTH),
                            channels=Constants.CHANNELS,
                            rate=Constants.RATE,
                            output=True)
        stream.write(audio.data)
