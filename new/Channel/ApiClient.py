#! /usr/bin/env python3
# -*- coding: utf-8 -*-


#####################################################
# PURPOSE: Clase que permite hacer uso de la api del#
#           contacto                                #
#                                                   #
# Vilchis Dominguez Miguel Alonso                   #
#       <mvilchis@ciencias.unam.mx>                 #
#                                                   #
# Notes:                                            #
#                                                   #
# Copyright   17-08-2015                            #
#                                                   #
# Distributed under terms of the MIT license.       #
#####################################################
from xmlrpc.client import ServerProxy
from Constants import CHAT_PORT
from AuxiliarFunctions import *

"""**************************************************
Clase que genera un proxy para poder hacer uso de
los procedimientos remotos que ofrece la api del contacto
**************************************************"""
class MyApiClient:
    def __init__(self, header, contact_ip = None, contact_port = None):
        self.header = header

        if contact_port:
            self.contact_proxy = ServerProxy('http://localhost:%i'%int(contact_port), allow_none=True)
        elif contact_ip:
            self.contact_proxy = ServerProxy('http://%s:%i'%(contact_ip, CHAT_PORT), allow_none=True)
        else:
            raise ValueError('The values of fields are not consistent MyApiClient.__init__')

    def send_text(self, text):
        message = self.header + text
        self.contact_proxy.send_message_wrapper(message)
