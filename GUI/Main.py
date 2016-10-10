#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from Constants.Constants import *
from GUI.Login import LocalLoginScreen, RemoteLoginScreen, ConnectScreen, UserAddScreen
from GUI.Chat import MainScreen
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

class ChatApp(App):
    def __init__(self, local_mode):
        super(ChatApp, self).__init__()

        self.sm = ScreenManager()
        if local_mode:
            login = LocalLoginScreen(name="login")
        else:
            login = RemoteLoginScreen(name="login")
        self.sm.add_widget(login)
        self.sm.current = "login"
        Window.clearcolor = RGBA_BG
        Window.size = (LOGIN_WIDTH, LOGIN_HEIGTH)

    def build(self):
        return self.sm

    def on_stop(self):
        print("Leaving")
        screen = self.sm.current_screen
        c_class = type(screen)

        if c_class is MainScreen and screen.session_active:
            print("[info] Logging out..")
            screen.log_out()
        elif c_class is ConnectScreen or c_class is UserAddScreen:
            print("[info] Shutting down server..")
            screen.channel.api_server.stop()
