#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from Constants.Constants import *
from .ApiServer import MyApiServer
from .ApiClient import MyApiClient

class Channel:
    def __init__(self, gui, contact_port=None, contact_ip=None, my_port=CHAT_PORT):
        self.api_server = MyApiServer(gui, my_port)
        self.api_client = MyApiClient(contact_ip, contact_port)

    def send_text(self, text):
        self.api_client.proxy.sendMessage_wrapper(text)
        
