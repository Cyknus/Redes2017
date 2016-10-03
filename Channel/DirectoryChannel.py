#! /usr/bin/env python3
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

from Channel.Channels import BidirectionalChannel
from Channel.ApiClient import *
from Channel.ApiServer import *
from Constants.Constants import *
from Constants.AuxiliarFunctions import *
from xmlrpc.client import ProtocolError
from threading import Thread

LOCALHOST = get_ip_address()

class DirectoryChannel(BidirectionalChannel):
    def __init__ (self, gui_parent, directory_ip, directory_port, my_port=CHAT_PORT):
        self.api_client = MyApiClient(directory_ip, directory_port)
        self.api_server = MyApiServer(gui_parent, my_port)

        self.api_server_thread = Thread(target=self.api_server.run, name="LocalServer")
        self.api_server_thread.start()

    """**************************************************
    Metodo que se encarga de obtener lista de contactos
    **************************************************"""
    def get_contacts(self, username):
        try:
            res = self.api_client.proxy.get_contacts_wrapper(username)
            return res["detailedInfo"]
        except ProtocolError as err:
            raise RuntimeError(err.errmsg)

    """**************************************************
    Metodo que se encarga de  conectar al contacto
    **************************************************"""
    def connect(self, username):
        try:
            res = self.api_client.proxy.username_available_wrapper(username)
            if res["detailedInfo"]:
                res_directory = self.api_client.proxy.connect_wrapper(
                    self.api_server.ip,
                    self.api_server.port,
                    username
                )
                if res_directory["status"] == OK:
                    return res_directory["detailedInfo"]
                else:
                    raise Exception(res_directory["detailedInfo"])
            else:
                raise ValueError("Username not available")
        except ProtocolError as err:
            raise RuntimeError(err.errmsg)

    """**************************************************
    Metodo que se encarga de  conectar al contacto
    **************************************************"""
    def disconnect(self, username):
        try:
            res = self.api_client.proxy.disconnect_wrapper(username)
            return res["detailedInfo"]
        except ProtocolError as err:
            raise RuntimeError(err.errmsg)
