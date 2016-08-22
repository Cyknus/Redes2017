#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from Constants import *
from .Channel import Channel
from GUI.ikivy import MyLabel

class MyApiClient:
    def  __init__(self):
        """ Constructor de la clase. Establece el canal en el puerto dado """
        self.proxy = None # al que se mandan mensajes
        self.server = None # servidor asociado

        # GUI
        self.display = None # donde se agregarán los mensajes

    def receive(self, message):
        msg = MyLabel(text=message, color=Constants.RGB_RECD)
        self.display.add_widget(msg)
