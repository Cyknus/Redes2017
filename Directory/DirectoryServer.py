#! /usr/bin/env python3
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
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import sys
sys.path.append("../")
from Constants.AuxiliarFunctions import *
from Constants.Constants import *

LOCALHOST = get_ip_address()

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
    def __init__(self, port=SERVER_PORT):
        self.client_dictionary = {}
        wrapper = FunctionWrapperDirectory(self.client_dictionary)

        self.server = SimpleXMLRPCServer((LOCALHOST, int(port)), requestHandler=RequestHandler)
        self.server.register_introspection_functions()
        self.server.register_multicall_functions()
        self.server.register_instance(wrapper)

        print("Directorio de ubicacion activo, mi direccion es:")
        print("(%s, %s)"%(LOCALHOST, port))

    def run(self):
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.shutdown()
            self.server.server_close()

class FunctionWrapperDirectory:
    """ **************************************************
    Constructor de la clase
    @clients_dictionary (Diccionario) Contiene la información de
                todos los clientes (Usa username como llave, y contiene el nombre del usuario)
    ************************************************** """
    def __init__(self, client_dictionary):
        self.client_dictionary = client_dictionary

    def get_contacts_wrapper(self,  username):
        print("[info] Retrieving contacts list to " + username)
        return {"status": OK, "detailedInfo": {k:v for k, v in self.client_dictionary.items() if k != username}}

    def connect_wrapper(self, ip_string, port_string, username):
        if username in self.client_dictionary:
            return {"status": ERROR, "detailedInfo": "Username already exist"}
        else:
            print("[info] Added " + username + " to directory")

            self.client_dictionary[username] = {
                NAME_CONTACT: username,
                IP_CONTACT: ip_string,
                PORT_CONTACT: port_string
            }
            return {"status": OK, "detailedInfo": self.get_contacts_wrapper(username)["detailedInfo"]}

    def disconnect_wrapper(self, username):
        self.client_dictionary.pop(username)
        return {"status": OK, "detailedInfo": "Connection closed"}

    def username_available_wrapper(self, username):
        print("[info] Looking availability for " + username)
        return {"status": OK, "detailedInfo": not (username in self.client_dictionary)}

# **************************************************
#  Definicion de la funcion principal
#**************************************************
def main(port):
    try:
        if port:
            general_server = GeneralDirectory(port)
        else:
            general_server = GeneralDirectory()
        general_server.run()
    except OSError as err:
        print("[error] Can't raise server:: " + err.strerror)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Run directory server for chat")
    parser.add_argument('-l', '--local', type=int, required=False, help='Runs in local mode on port PORT', dest='local', metavar='PORT')
    args = parser.parse_args()
    main(args.local)
