#! /usr/bin/env python
# -*- coding: utf-8 -*-


#####################################################
# PURPOSE: Clase que representa la abstracción de   #
#         Un canal bidireccional (con el servido de #
#         ubicacion), haciendo  uso de la biblioteca#
#         xmlRpc                                    #
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

from ApiServer import *
from Channels import *
from Constants import CHAT_PORT
from AuxiliarFunctions import *

class DirectoryChannel(BidirectionalChannel):
    def __init__ (self,Qpartent,directory_ip = None, my_port = None, directory_port = None, username = None):
        super(DirectoryChannel, self).__init__(gui_parent, directory_ip, directory_port, my_port)

    """**************************************************
    Metodo que se encarga de obtener lista de contactos
    **************************************************"""
    def get_contacts(self):
        #TODO
    """**************************************************
    Metodo que se encarga de  conectar al contacto
    **************************************************"""
    def connect(self):
        #TODO
    """**************************************************
    Metodo que se encarga de  conectar al contacto
    **************************************************"""
    def disconnect(self):
        #TODO
