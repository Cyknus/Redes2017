#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from Channel.Channel import Channel
from Channel.ApiClient import MyApiClient
from Constants import *

Window.clearcolor = Constants.RGBA_BG

# Descripción de las ventanas
Builder.load_file('GUI/screens.kv')
# Para manejar las pantallas
sm = ScreenManager()
# El cliente que se levanta
client = MyApiClient()

class LocalLoginScreen(Screen):
    def accessRequest(self, my_port, contact_port):
        """ Ingreso de modo local """
        client.proxy = Channel.connect_to(contact_port=contact_port)
        client.server = Channel.server_up(client, my_port)
        print("Conexión establecida entre " + str(my_port) + " hacia " + str(contact_port))

        # lanzar la siguiente ventana
        sm.current = "chat"
        Window.size = Constants.CHAT_SIZE

class RemoteLoginScreen(Screen):
    def accessRequest(self, contact_ip):
        """ Ingreso de modo remoto """
        client.proxy = Channel.connect_to(contact_ip=contact_ip)
        client.server = Channel.server_up(client)
        print("Conexión establecida hacia " + str(contact_ip))

        # lanzar la siguiente ventana
        sm.current = "chat"
        Window.size = Constants.CHAT_SIZE

class ChatScreen(Screen):
    def send(self, text):
        client.proxy.sendMessage_wrapper(text)
        # aquí tiene que aparecer en pantalla el último enviado
        msg = MyLabel(text=text, color=Constants.RGB_SEND)
        client.display.add_widget(msg)
        # limpiar lo que está escrito
        self.ids.block_of_typos.text = ''

# dummy class
class ChatApp(App):
    def build(self):
        return sm

    def on_stop(self):
        client.server.close()

# better label
class MyLabel(Label):
    def __init__(self, color, halign='right'):
        super(MyLabel, self).__init__()
        self.size_hint = Constants.SIZE_HINT_MSG
        self.height = Constants.MSG_HEIGHT
        self.color = color
        self.text_size = self.size

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
