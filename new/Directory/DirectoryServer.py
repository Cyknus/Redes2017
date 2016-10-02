#! /usr/bin/env python
# -*- coding: utf-8 -*-


#####################################################
# PURPOSE: Clase que manejara los clientes que se   #
#          conectan y desconectan al sistema        #
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
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

#           Mis bibliotecas
import sys,getopt
sys.path.insert(0, '../')
sys.path.insert(0, 'Constants')
from AuxiliarFunctions import *
from Constants import *
# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class GeneralDirectory:
    """ Constructor de la clase, si recibe un puerto, entonces
        Trabajara de manera local, de otra manera, utilizará  la ip
        con la que cuenta.
        @param port <int> Si trabaja de manera local, representa el
                        número del puerto por el cual recibirá las peticiones
    """
    def __init__(self, port = None):
        #TODO
        self.client_dictionary = {}
        funtionWrapper = FunctionWrapperDirectory(self.client_dictionary)
        print "Directorio de ubicacion activo, mi direccion es:"
        print "(%s, %s)" %(get_ip_address(), port)


class FunctionWrapperDirectory:
    """ **************************************************
    Constructor de la clase
    @clients_dictionary (Diccionario) Contiene la información de
                todos los clientes (Usa username como llave, y contiene el nombre del usuario)
    ************************************************** """
    def __init__(self,client_dictionary):
        self.client_dictionary = client_dictionary


    def get_contacts_wrapper(self,  username):
        #TODO

    def connect_wrapper(self, ip_string, port_string, username):
        #Las llaves del diccionario de un cliente debe usar las 
        #llaves que se encuentran en las constantes:
            #NAME_CONTACT
            #IP_CONTACT
            # PORT_CONTACT
           
        #TODO

    def disconnect_wrapper(self, ip_string, port_string):
        #TODO

# **************************************************
#  Definicion de la funcion principal
#**************************************************
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "l", ["local="])
    except getopt.GetoptError:
        print 'Uso con puertos locales:'
        print '$ python Directory/DirectoryServer.py -l <puerto>'
        print 'Uso entre computadoras dentro de la red'
        print '$ python Directory/DirectoryServer.py '
        sys.exit(2)
    if opts: #Si el usuario mandó alguna bandera
        local = True if '-l' in opts[0] else False
        if local:
            general_server = GeneralDirectory(port = args[0]).server
        else:
            general_server = GeneralDirectory().server
        general_server.serve_forever()


if __name__ == '__main__':
    main(sys.argv[1:])
