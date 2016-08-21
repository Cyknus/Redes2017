#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from Constants import *
from .Channel import Channel

class MyApiClient: # wtf?
    def  __init__(self, my_port = Constants.CHAT_PORT):
        """ Constructor de la clase. Establece el canal en el puerto dado """
        self.channel = Channel(self, my_port)

    def connect_local(self, contact_port):
        self.channel.connect_to(contact_port=contact_port)

    def connect_remote(self, contact_ip):
        self.channel.connect_to(contact_ip=contact_ip)

    def send(self, message):
        self.channel.send_text(message)

    def receive(self, message):
        pass # TODO aqui marcamos en la GUI
