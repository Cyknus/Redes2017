#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import json
from threading import Thread, Lock
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import sys
sys.path.append("../")
from Channel.Channels import RequestChannel
from Constants.AuxiliarFunctions import *
from Constants.Constants import *
from Services.Decorators import build_response, encrypt_password
from Services.Logger import *

lock = Lock()

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class GeneralDirectory:
    def __init__(self, port=SERVER_PORT):
        self.client_dictionary = {}
        self.database = json.load(open('database.db'))

        wrapper = FunctionWrapperDirectory(self.client_dictionary, self.database)

        self.server = SimpleXMLRPCServer((get_ip_address(), int(port)), requestHandler=RequestHandler)
        self.server.register_introspection_functions()
        self.server.register_instance(wrapper)

        self.log = Logger.getFor("GeneralDirectory")
        self.log.info("Directorio de ubicacion activo, mi direccion es:")
        self.log.info("(%s, %s)"%(get_ip_address(), port))

        self.thread_contacts = Thread(target=self.ping_contacts, name="ContactsThread")
        self.thread_contacts.start()

    def run(self):
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
        finally:
            json.dump(self.database, open('database.db', 'w'))
            self.thread_contacts.join()

    def ping_contacts(self):
        while self.server:
            with lock:
                contacts = self.client_dictionary.items()
                self.log.debug(self.client_dictionary.keys())

            for k, v in contacts:
                proxy = v[CHANNEL_CONTACT].api_client.proxy
                try:
                    proxy.ping_wrapper()
                except:
                    with lock:
                        self.client_dictionary.pop(k)
                        _contacts = self.client_dictionary.items()

                    for _k, _v in _contacts:
                        _proxy = _v[CHANNEL_CONTACT].api_client.proxy
                        _proxy.remove_contact(k)
            time.sleep(5)

class FunctionWrapperDirectory:
    def __init__(self, client_dictionary, database):
        self.client_dictionary = client_dictionary
        self.database = database
        self.log = Logger.getFor("FunctionWrapper")

    @build_response
    def get_contacts_wrapper(self,  username):
        self.log.info("Retrieving contacts to %s", username)
        return OK, { k: { k:v for k, v in self.client_dictionary[k].items() if k != CHANNEL_CONTACT }
            for k, v in self.client_dictionary.items() if k != username }

    @build_response
    def connect_wrapper(self, ip_string, port_string, username):
        if username not in self.database:
            return ERROR, "Not found user"
        elif username in self.client_dictionary:
            return OK, "Username already connected"
        else:
            with lock:
                _contacts = self.client_dictionary.items()

            for _k, _v in _contacts:
                _proxy = _v[CHANNEL_CONTACT].api_client.proxy
                _proxy.add_contact(username, ip_string, port_string)

            req_channel = RequestChannel(ip_string, port_string)

            with lock:
                self.client_dictionary[username] = {
                        NAME_CONTACT: username,
                        IP_CONTACT: ip_string,
                        PORT_CONTACT: port_string,
                        CHANNEL_CONTACT: req_channel
                        }

            self.log.info("Added %s to directory", username)
            res = self.get_contacts_wrapper(username)
            return res[STATUS], res[MESSAGE]

    @build_response
    def disconnect_wrapper(self, username):
        with lock:
            self.client_dictionary.pop(username)
            _contacts = self.client_dictionary.items()

        for _k, _v in _contacts:
            _proxy = _v[CHANNEL_CONTACT].api_client.proxy
            _proxy.remove_contact(username)
        return OK, "Connection closed"

    @build_response
    def username_available_wrapper(self, username):
        self.log.debug("Looking availability for %s", username)
        return OK, not (username in self.database)

    @encrypt_password
    @build_response
    def do_log_in_wrapper(self, username, password):
        if username not in self.database:
            return ERROR, "User doesn't exist"

        if self.database[username] == password:
            return OK, True
        else:
            return ERROR, "Incorrect combination"

    @encrypt_password
    @build_response
    def do_sign_up_wrapper(self, username, password):
        if username in self.database:
            return ERROR, "username already registered"

        self.database[username] = password
        return OK, True

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
