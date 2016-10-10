#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from Channel.Channels import BidirectionalChannel
from Channel.ApiClient import *
from Channel.ApiServer import *
from Constants.Constants import *
from Constants.AuxiliarFunctions import *
from Services.Logger import *
from Services.Decorators import build_response, try_catch
from xmlrpc.client import ProtocolError
from threading import Thread

class DirectoryChannel(BidirectionalChannel):
    def __init__ (self, gui_parent, directory_ip, directory_port, my_port=CHAT_PORT):
        self.api_client = MyApiClient(directory_ip, directory_port)
        self.api_server = MyApiServer(gui_parent, my_port)

        self.api_server_thread = Thread(target=self.api_server.run, name="LocalServer")
        self.api_server_thread.start()

        self.log = Logger.getFor("DirectoryChannel")

    @try_catch
    def get_contacts(self, username):
        res = self.api_client.proxy.get_contacts_wrapper(username)
        return res[MESSAGE]

    @try_catch
    def connect(self, username):
        res = self.api_client.proxy.username_available_wrapper(username)
        if res[MESSAGE]:
            res_directory = self.api_client.proxy.connect_wrapper(
                self.api_server.ip,
                self.api_server.port,
                username
            )
            if res_directory[STATUS] == OK:
                return res_directory[MESSAGE]
            raise ConnectionAbortedError(res_directory[MESSAGE])
        else:
            raise ValueError("Username not available")

    @try_catch
    def disconnect(self, username):
        res = self.api_client.proxy.disconnect_wrapper(username)
        return res[MESSAGE]
