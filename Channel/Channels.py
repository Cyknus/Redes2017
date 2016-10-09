#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from Channel.ApiClient import *
from Channel.ApiServer import *
from Constants.Constants import *
from Services.Decorators import try_catch, parse_params
from Services.Logger import *
from threading import Thread

class RequestChannel():
    """
        Represents the a one-direction channel
        It has one proxy pointing to the server

        @param contact_ip - server IP Address
        @param contact_port - server Port
    """

    @parse_params
    def __init__(self, contact_ip, contact_port):
        self.api_client = MyApiClient(contact_ip, contact_port)
        self.contact_ip = contact_ip
        self.contact_port = contact_port
        self.log = Logger.getFor("RequestChannel")

    @try_catch
    def send_text(self, text):
        self.log.debug("Sending message to %s:%d", self.contact_ip, self.contact_port)

        res = self.api_client.proxy.send_message_wrapper(text)
        if res[STATUS] == ERROR:
            self.log.error("Request failed: %s", res[MESSAGE])
            raise ConnectionRefusedError()
        elif res[STATUS] == OK:
            self.log.info("Got response: %s", res[MESSAGE])
            return

        raise NotImplementedError()

    @try_catch
    def new_connection(self, my_ip, my_port, username):
        self.log.debug("Creating connection with %s:%d", self.contact_ip, self.contact_port)

        res = self.api_client.proxy.new_chat_wrapper(my_ip, my_port, username)
        if res[STATUS] == ERROR:
            self.log.error("Unexpected response: %s", res[MESSAGE])
            raise ValueError()
        elif res[STATUS] == OK:
            self.log.info("Got response: %s", res[MESSAGE])
            return

        raise NotImplementedError()

    @try_catch
    def begin_call(self, call):
        self.log.debug("Beginning call with %s:%d", self.contact_ip, self.contact_port)

        res = self.api_client.proxy.new_call_wrapper(call)
        if res[STATUS] == ERROR:
            self.log.error("Unexpected response: %s", res[MESSAGE])
            raise ValueError()
        elif res[STATUS] == OK:
            self.log.debug("Got response: %s", res[MESSAGE])

    def send_bytes(self, data):
        try:
            print("[info] Streaming..")
            res = self.api_client.proxy.play_audio_wrapper(data)
            # Handle error from playing the other side
            return res["detailedInfo"]
        except ProtocolError as err:
            raise RuntimeError("Can't send bytes")

    ### Getters
    def get_api_client(self):
        return self.api_client


class BidirectionalChannel(RequestChannel):
    def __init__(self, gui_parent, contact_ip=None, contact_port=None, my_port=None):
        if my_port and contact_port:
            self.api_client = MyApiClient(contact_port=contact_port)
            self.api_server = MyApiServer(gui_parent, my_port)
        elif contact_ip:
            self.api_client = MyApiClient(contact_ip= contact_ip)
            self.api_server = MyApiServer(gui_parent)
        else:
            raise ValueError('The values of fields are not consistent BidirectionalChannel.__init__')

        self.api_server_thread = Thread(target=self.api_server.run)
        self.api_server_thread.start()

    """**************************************************
    Metodos Get
    **************************************************"""
    def get_api_server(self):
        return self.api_server_thread
