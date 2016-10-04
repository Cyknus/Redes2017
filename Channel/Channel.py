#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from Constants.Constants import *
from .ApiServer import MyApiServer
from .ApiClient import MyApiClient
from xmlrpc.client import Binary

class Channel:
    def __init__(self, gui, contact_port=None, contact_ip=None, my_port=CHAT_PORT):
        self.api_server = MyApiServer(gui, my_port)
        self.api_client = MyApiClient(contact_ip, contact_port)

    def send_text(self, text):
        res = self.api_client.proxy.sendMessage_wrapper(text)
        print("Contact response " + res)

    def send_bytes(self, in_data):
        d = Binary(in_data)
        res = self.api_client.proxy.sendAudio_wrapper(d)
        print("Contact responde " + res)
