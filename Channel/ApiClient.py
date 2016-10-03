#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from xmlrpc.client import ServerProxy
from Constants.Constants import *
from Constants.AuxiliarFunctions import get_ip_address

LOCALHOST = get_ip_address()

class MyApiClient:
    def __init__(self, contact_ip=LOCALHOST, contact_port=CHAT_PORT):
        self.proxy = ServerProxy('http://%s:%i'%(contact_ip, int(contact_port)), allow_none=True)
