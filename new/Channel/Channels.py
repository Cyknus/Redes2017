#! /usr/bin/env python3
# -*- coding: utf-8 -*-


#####################################################
# PURPOSE: Clase que representa la abstracción de   #
#         Un canal bidireccional, con uso de la     #
#          biblioteca xmlRpc                        #
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
from ApiClient import *
from threading import Thread

"""**************************************************
Las instancias de esta clase contendran los metodos
necesarios para hacer uso de los metodos
del api de un contacto. Internamente Trabajara
con una proxy apuntando hacia los servicios del
servidor xmlrpc del contacto
**************************************************"""
class RequestChannel():
    """**************************************************
    Constructor de la clase
    @param <str> contact_ip: Si no se trabaja de manera local
                representa la ip del contacto con el que se
                establecera la conexion
    @param <int> contact_port: De trabajar de manera local
                representa el puerto de la instancia del contacto
    **************************************************"""
    def __init__(self, header, contact_ip = None, contact_port = None):
        self.api_client = ApiClient(header, contact_ip, contact_port)

    """**************************************************
    Metodo que se encarga de mandar texto al contacto con
    el cual se estableció la conexion
    **************************************************"""
    def send_text(self, text):
        self.api_client.send_text(text)

    """**************************************************
    Metodo que se encarga de mandar iniciar una conversacion
    con un nuevo contacto
    **************************************************"""
    def new_connection(self, my_ip, my_port, username):
        self.api_client.new_chat_wrapper(my_ip, my_port, username)

    """**************************************************
    Metodo que se encarga de mandar audio y video al contacto
    con el cual se estableció la conexion
    **************************************************"""
    def begin_call(self):
        #TODO

    """**************************************************
    Metodos Get
    **************************************************"""
    def get_api_client(self):
        return self.api_client


class BidirectionalChannel(RequestChannel):
    def __init__(self, gui_parent, contact_ip = None,  contact_port = None,my_port = None):
        if my_port and contact_port:
            self.api_client = ApiClient(contact_port= contact_port)
            self.api_server = ApiServer(gui_parent, my_port)
        elif contact_ip:
            self.api_client = ApiClient(contact_ip= contact_ip)
            self.api_server = ApiServer(gui_parent)
        else:
            raise ValueError('The values of fields are not consistent BidirectionalChannel.__init__')

        self.api_server_thread = Thread(target=self.api_server.run)
        self.api_server_thread.start()

    """**************************************************
    Metodos Get
    **************************************************"""
    def get_api_server(self):
        return self.api_server_thread
