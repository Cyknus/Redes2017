#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from Channel.ApiClient import MyApiClient
from Constants import *

Window.clearcolor = Constants.RGBA_BG

# Descripción de las ventanas
Builder.load_file('GUI/screens.kv')
# Para manejar las pantallas
sm = ScreenManager()


class LocalLoginScreen(Screen):
    """ Clase que describe las acciones disponibles en la pantalla de acceso"""

    def accessRequest(self, my_port, contact_port):
        """ Ingreso de modo local """
        sm.current = "chat"
        Window.size = Constants.CHAT_SIZE

class RemoteLoginScreen(Screen):
    def accessRequest(self, contact_ip):
        """ Ingreso de modo remoto """
        sm.current = "chat"
        Window.size = Constants.CHAT_SIZE

class ChatScreen(Screen):
    def send(self, text): # TODO ligar con ApiClient
        pass

# dummy class
class ChatApp(App):
    def build(self):
        return sm

def build_screen_manager(local):
    if local:
        sm.add_widget(LocalLoginScreen(name="login"))
        size = Constants.SIZE_LL
    else:
        sm.add_widget(RemoteLoginScreen(name="login"))
        size = Constants.SIZE_RL

    # set scroll view
    root = ChatScreen(name="chat")
    sm.add_widget(root)

    # Make sure the height is such that there is something to scroll.
    root.ids.layout.bind(minimum_height=root.ids.layout.setter('height'))
    # Así es como se agregan cosas..
    for i in range(40):
        btn = Label(text=str(i), size_hint_y=None, height=40, color=(0,0,0,1))
        root.ids.layout.add_widget(btn)

    chat = ChatApp()
    Window.size = size

    return chat
