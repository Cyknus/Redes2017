#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from Channel.DirectoryChannel import DirectoryChannel
from Constants.Constants import *
from GUI.Chat import MainScreen
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from Services.Logger import *

Builder.load_file('GUI/kivy/login_screens.kv')

class LoginManager(Screen):
    def __init__(self, **kwargs):
        super(LoginManager, self).__init__(**kwargs)
        self.log = Logger.getFor("LoginManager")

    def doLogin(self, server_ip, server_port, my_port=None):
        try:
            self.log.info("Connecting with server at %s:%s", server_ip, server_port)
            directory = DirectoryChannel(self.manager, server_ip, server_port, my_port)
            connect = ConnectScreen(directory=directory)
            self.manager.add_widget(UserAddScreen(directory=directory))
            self.manager.switch_to(connect)
        except OSError as err:
            self.log.error("Can't create connections: %s", err)

class LocalLoginScreen(LoginManager):
    def accessRequest(self, my_port, server_address, server_port):
        self.log.debug("Chat in local mode")
        self.doLogin(server_address, server_port, my_port)

class RemoteLoginScreen(LoginManager):
    def accessRequest(self, server_address, server_port):
        self.log.debug("Chat in remote mode")
        self.doLogin(server_address, server_port)

class UserAddScreen(Screen):
    def __init__(self, directory, **kwargs):
        super(UserAddScreen, self).__init__(**kwargs)
        self.channel = directory
        self.log = Logger.getFor("UserAddScreen")

    def user_add(self, username, passw, cpassw):
        if username == '' or passw == '' or cpassw == '':
            self.log.error("No data provided")
            return

        if passw != cpassw:
            self.log.error("Passwords don't match")
            return

        try:
            dict_contacts = self.channel.register(username, passw)
            main_app = MainScreen(username=username, channel=self.channel, name="main")
        except Exception as e:
            self.log.error("Sign up failed: %s", e)
        else:
            self.log.info("Logged as %s", username)
            main_app.ids.contacts_list.load_contacts(dict_contacts)
            Window.size = (MAIN_WIDTH, MAIN_HEIGHT)
            self.manager.switch_to(main_app)

class ConnectScreen(Screen):
    def __init__(self, directory, **kwargs):
        super(ConnectScreen, self).__init__(**kwargs)
        self.channel = directory
        self.log = Logger.getFor("ConnectScreen")

    def connect(self, username, password):
        if username == '' or password == '':
            self.log.error("No data provided")
            return

        try:
            dict_contacts = self.channel.connect(username, password)
            main_app = MainScreen(username=username, channel=self.channel, name="main")
        except Exception as e:
            self.log.error("Log in failed: %s", e)
        else:
            self.log.info("Logged as %s", username)
            main_app.ids.contacts_list.load_contacts(dict_contacts)
            Window.size = (MAIN_WIDTH, MAIN_HEIGHT)
            self.manager.switch_to(main_app)
