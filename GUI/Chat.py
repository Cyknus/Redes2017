#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

from ApiClient import MyApiClient

# Descripción de las ventanas
Builder.load_file('GUI/screens.kv')
# Para manejar las pantallas
sm = ScreenManager()

class LocalLoginScreen(Screen):
    """ Clase que describe las acciones disponibles en la pantalla de acceso"""

    def accessRequest(self, my_port, contact_port):
        """ Ingreso de modo local """
        sm.current = "chat"

class RemoteLoginScreen(Screen):
    def accessRequest(self, contact_ip):
        """ Ingreso de modo remoto """
        sm.current = "chat"

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
    else:
        sm.add_widget(RemoteLoginScreen(name="login"))
    sm.add_widget(ChatScreen(name="chat"))

    return ChatApp()
