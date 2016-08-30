#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from Constants.AuxiliarFunctions import *
from xmlrpc.client import ServerProxy

class MyApiClient:
    def  __init__(self, contact_ip=None, contact_port=None):
        if contact_ip:
            contact_server = ServerProxy('http://%s:%i'%(contact_ip, int(contact_port)), allow_none=True)
        else:
            contact_server = ServerProxy('http://%s:%i'%(get_ip_address(), int(contact_port)), allow_none=True)

        self.proxy = contact_server

    def play(self, audio):
        self.display.play(audio) # porquenosgustapasaralassiguientesfunciones
