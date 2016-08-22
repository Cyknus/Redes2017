#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from Constants import *
from .Channel import Channel
from GUI.Chat import MyLabel

class MyApiClient:
    def  __init__(self):
        """ Constructor de la clase. Establece el canal en el puerto dado """
        self.proxy = None # al que se mandan mensajes
        self.server = None # servidor asociado

        # GUI
        self.display = None # donde se agregarán los mensajes

    def receive(self, message):
        msg = Label(text=message, color=Constants.RGB_RECD, halign='left')
        self.display.add_widget(msg)
