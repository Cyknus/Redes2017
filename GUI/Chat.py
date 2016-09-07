#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import gi

gi.require_version('Gtk', '3.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from .ikivy import MyLabel

from Channel.Channel import Channel
from Channel.ApiClient import MyApiClient
from Constants import *

Window.clearcolor = Constants.RGBA_BG

# Descripción de las ventanas
Builder.load_file('GUI/screens.kv')
# Para manejar las pantallas
sm = ScreenManager()
# El cliente que se levanta
channel = Channel()
client = MyApiClient()

class LocalLoginScreen(Screen):
    def accessRequest(self, my_port, contact_port):
        """ Ingreso de modo local """
        try:
            channel.connect_to(contact_port=contact_port)
            channel.server_up(client, my_port)
            print("Conexión establecida entre " + str(my_port) + " hacia " + str(contact_port))

            # lanzar la siguiente ventana
            sm.current = "chat"
            Window.size = Constants.CHAT_SIZE
        except Exception as e:
            if channel.server is not None:
                channel.server_down()
            print("No se ha podido establecer una conexión. Intenta de nuevo.")

class RemoteLoginScreen(Screen):
    def accessRequest(self, contact_ip):
        """ Ingreso de modo remoto """
        try:
            connect_to(contact_ip=contact_ip)
            server_up(client)
            print("Conexión establecida hacia " + str(contact_ip))

	        # lanzar la siguiente ventana
            sm.current = "chat"
            Window.size = Constants.CHAT_SIZE
        except Exception as e:
            if channel.server is not None:
                channel.server_down()
            print("No se ha podido establecer una conexión. Intenta de nuevo")

class ChatScreen(Screen):
    def send(self, text):
        try:
            channel.send_text(text)
            # aquí tiene que aparecer en pantalla el último enviado
            msg = MyLabel(text=text, color=Constants.RGB_SEND)
        except Exception as e:
            msg = MyLabel(text=text, color=Constants.RGB_NSEND)
            print("Mensaje no ha podido ser enviado.")

        client.display.add_widget(msg)
        # limpiar lo que está escrito
        self.ids.block_of_typos.text = ''

# dummy class
class ChatApp(App):
    def build(self):
        return sm

    def on_stop(self):
        if channel.server is not None:
            channel.server_down()

# acoplar todo
def build_screen_manager(local):
    if local:
        sm.add_widget(LocalLoginScreen(name="login"))
        size = Constants.SIZE_LL
    else:
        sm.add_widget(RemoteLoginScreen(name="login"))
        size = Constants.SIZE_RL

    Window.size = size # tamaño de acuerdo al login
    # set scroll view
    root = ChatScreen(name="chat")
    sm.add_widget(root)

    # Make sure the height is such that there is something to scroll.
    root.ids.layout.bind(minimum_height=root.ids.layout.setter('height'))
    client.display = root.ids.layout

    # creamos la aplicación
    chat = ChatApp()

    return chat
