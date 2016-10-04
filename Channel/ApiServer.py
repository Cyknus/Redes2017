#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from Constants.Constants import *
from Constants.AuxiliarFunctions import *
from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread
import pyaudio

class MyApiServer:
    def __init__(self, gui, my_port=CHAT_PORT):
        wrapper = FunctionWrapper(gui)
        # configuración de xmlrpc.. todo se hace aquí
        xmlrpc_server = SimpleXMLRPCServer((get_ip_address(), int(my_port)))
        xmlrpc_server.register_introspection_functions()
        xmlrpc_server.register_instance(wrapper)
        # lanzar servidor
        api_server_thread = Thread(target=xmlrpc_server.serve_forever)
        api_server_thread.start()
        # guardar instancia para poder matar el hilo después
        self.server = xmlrpc_server

    def stop(self):
        self.server.shutdown()
        self.server.server_close()

class FunctionWrapper:
    def __init__(self, gui):
        self.gui = gui

    def sendMessage_wrapper(self, message):
        self.gui.current_screen.display_message(message)
        return "OK"

    def sendAudio_wrapper(self, d):
        self.gui.current_screen.listen_audio(d.data)
        return "OK"
