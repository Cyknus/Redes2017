#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from Constants.AuxiliarFunctions import *
from Constants.Constants import *
from Services.Decorators import build_response, decode_message
from Services.Logger import *
from socketserver import TCPServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer
import threading

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class MyApiServer:
    """
        User server class. Through this contacts send messages to the user.

        @param gui_parent - GUI element with methods (current_screen)
                                entry_message
                                entry_connection
                                entry_audio_call
        @param my_port - Default: 5000 - Port in which server runs
    """
    def __init__(self, gui_parent, my_port=None):
        self.port = int(my_port) if my_port else CHAT_PORT
        self.ip = get_ip_address()
        self.chats_dictionary = {}
        # configurar el servidor
        wrapper = FunctionWrapper(gui_parent, self.chats_dictionary)
        self.server = Server((self.ip, self.port), requestHandler=RequestHandler)
        self.server.register_instance(wrapper)
        # get logger
        self.log = Logger.getFor("MyApiServer")
        self.log.debug("Local server initialized")

    def run(self):
        try:
            self.log.info("Local server running at %s:%d", self.ip, self.port)
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.close()

    def stop(self):
        self.log.info("Shutting down server")
        self.server.close()

    def remove_chat(self, username):
        self.chats_dictionary.pop(username)
        self.log.debug("Drop %s of chats_dictionary", username)
        self.log.debug("Current active chats:\n%s", str(self.chats_dictionary))

    def add_chat(self, contact):
        self.log.debug("Added %s in chats_dictionary", contact.username)
        self.chats_dictionary[contact.username] =  {
            IP_CONTACT: contact.ip_address,
            PORT_CONTACT: contact.port,
            'audio_call': False
        }

class FunctionWrapper:
    """
        Functions that local server offer
    """
    def __init__(self, gui_parent, chats_dictionary):
        self.gui_parent = gui_parent
        self.chats_dictionary = chats_dictionary # Handle entry connections
        self.log = Logger.getFor("FunctionWrapper")

    @build_response
    def new_chat_wrapper(self, contact_ip, contact_port, username):
        self.log.debug("New connection from %s@%s:%d", username, contact_ip, contact_port)

        if username not in self.chats_dictionary:
            self.gui_parent.current_screen.entry_connection(username, contact_ip, contact_port)
            self.chats_dictionary[username] = {
                IP_CONTACT: contact_ip,
                PORT_CONTACT: contact_port,
                'audio_call': False
            }

        return OK, "Connection ready"

    @decode_message
    @build_response
    def send_message_wrapper(self, contact_username, contact_ip, contact_port, text):
        self.log.debug("New message from %s@%s:%d", contact_username, contact_ip, contact_port)

        if contact_username in self.chats_dictionary:
            self.gui_parent.current_screen.entry_message(contact_username, contact_ip, contact_port, text)
            return OK, "Received"
        else:
            return ERROR, "Connection closed"

    def echo(self, message):
        pass

    @build_response
    def play_audio_wrapper(self,audio):
        if self.gui_parent.current_screen.active_stream:
            self.gui_parent.current_screen.play_audio(audio.data)
        return OK, "Received"

    def play_video_wrapper(self,frame):
        pass

    @decode_message
    @build_response
    def new_call_wrapper(self, contact_username, contact_ip, contact_port, typo):
        if contact_username not in self.chats_dictionary:
            return ERROR, "Connection Refused"

        if typo == AUDIO:
            self.log.debug("New call from %s@%s:%d", contact_username, contact_ip, contact_port)
            if username in self.chats_dictionary: # TODO: how to know if the call is already open?
                return OK, "Connection already open"

            self.gui_parent.current_screen.entry_audio_call(contact_username, contact_ip)
            # self.chats_dictionary[username]['audio_call'] = True
            return OK, "Connection ready"

        return ERROR, "Invalid Operation"

    @build_response
    def remove_contact(self, username):
        if username in self.chats_dictionary:
            self.chats_dictionary.pop(username)
            self.log.debug("Current online contacts: %s", self.chats_dictionary.keys())
            self.gui_parent.current_screen.remove_contact(username)

        return OK, "Contact {0} droped".format(username)

    @build_response
    def add_contact(self, username, ip, port):
        if username not in self.chats_dictionary:
            self.chats_dictionary[username] =  {
                IP_CONTACT: ip,
                PORT_CONTACT: port,
                'audio_call': False
            }
            self.log.debug("Current online contacts: %s", self.chats_dictionary.keys())
            self.gui_parent.current_screen.add_contact(username, ip, port)

        return OK, "Contact {0} added".format(username)

    def ping_wrapper(self):
        return True

class Server:
    def __init__(self, addr, requestHandler):
        self.socket = TCPServer(addr, requestHandler)

    def register_instance(self, object):


    def serve_forever(self):
        self.socket.serve_forever()

    def close(self):
        self.socket.shutdown()
        self.socket.server_close()
