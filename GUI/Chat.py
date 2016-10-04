#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import mainthread
from .ikivy import MyLabel

from Channel.Channel import Channel
from Constants.Constants import *

Window.clearcolor = RGBA_BG

# Descripción de las ventanas
Builder.load_file('GUI/screens.kv')

class LocalLoginScreen(Screen):
    def accessRequest(self, my_port, contact_port):
        """ Ingreso de modo local """
        try:
            channel = Channel(gui=self.manager, my_port=my_port, contact_port=contact_port)
            print("Conexión establecida entre " + str(my_port) + " hacia " + str(contact_port))

            # lanzar la siguiente ventana
            chat = ChatScreen(channel=channel, name="chat")
            self.manager.switch_to(chat)
            Window.size = CHAT_SIZE
        except Exception as e:
            print("No se ha podido establecer una conexión. Intenta de nuevo.")

class RemoteLoginScreen(Screen):
    def accessRequest(self, contact_ip):
        """ Ingreso de modo remoto """
        try:
            channel = Channel(gui=self.manager, contact_ip=contact_ip)
            print("Conexión establecida hacia " + str(contact_ip))

	        # lanzar la siguiente ventana
            chat = ChatScreen(channel=channel, name="chat")
            self.manager.switch_to(chat)
            Window.size = CHAT_SIZE
        except Exception as e:
            print("No se ha podido establecer una conexión. Intenta de nuevo")

class ChatScreen(Screen):
    def __init__(self, channel, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        self.ids.layout.bind(minimum_height=self.ids.layout.setter('height'))
        self.channel = channel

    def send(self, text):
        try:
            self.channel.send_text(text)
            # aquí tiene que aparecer en pantalla el último enviado
            msg = MyLabel(text=text, color=RGB_SEND)
        except Exception as e:
            print(e)
            msg = MyLabel(text=text, color=RGB_NSEND)
            print("Mensaje no ha podido ser enviado.")

        self.ids.layout.add_widget(msg)
        # limpiar lo que está escrito
        self.ids.block_of_typos.text = ''

    @mainthread
    def display_message(self, text):
        msg = MyLabel(text=text, color=RGB_RECD)
        self.ids.layout.add_widget(msg)

class ChatApp(App):
    def __init__(self, local_mode, **kwargs):
        super(ChatApp, self).__init__(**kwargs)
        self.sm = ScreenManager()
        if local_mode:
            self.sm.add_widget(LocalLoginScreen(name="login"))
            size = SIZE_LL
        else:
            self.sm.add_widget(RemoteLoginScreen(name="login"))
            size = SIZE_RL
        Window.size = size

    def build(self):
        return self.sm

    def on_stop(self):
        screen = self.sm.current_screen
        if type(screen) is ChatScreen:
            screen.channel.api_server.stop()
