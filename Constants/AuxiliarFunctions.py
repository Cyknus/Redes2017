#! /usr/bin/env python
# -*- coding: utf-8 -*-


#####################################################
# PURPOSE:Funciones auxiliares                      #
#                                                   #
# Vilchis Dominguez Miguel Alonso                   #
#       <mvilchis@ciencias.unam.mx>                 #
#                                                   #
# Notes:                                            #
#                                                   #
# Copyright   16-08-2015                            #
#                                                   #
# Distributed under terms of the MIT license.       #
#####################################################
import socket
import time
from Constants.Constants import *

"""**************************************************
 Metodo auxiliar que hace uso de internet para
 conocer la ip con la que contamos como usuarios
**************************************************"""

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return "%s"% (s.getsockname()[0])

def dummy_run(arg, **kwargs):
    while arg():
        time.sleep(0.1)

""" Funcion que construira el header del mensaje a mandar """
def get_message_header(username, ip):
    return username+':'+ip+':'

def split_message_header(message):
    message_split = message.split(':')
    message_text = ':'.join(message_split[MESSAGE_TEXT:])
    return (message_split[MESSAGE_USERNAME], message_split[MESSAGE_IP], message_text)
