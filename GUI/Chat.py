#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .ikivy import *
from Channel.Channels import RequestChannel
from Constants.Constants import *
from Constants.AuxiliarFunctions import get_message_header
from GUI.Utils import LogoutScreen
from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from Services.Logger import *

Builder.load_file('GUI/kivy/chat_screens.kv')

class MainScreen(Screen):
    def __init__(self, channel, username, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.channel = channel
        self.username = username
        self.header = get_message_header(self.username, self.channel.api_server.ip, self.channel.api_server.port)
        self.session_active = True
        self.log = Logger.getFor("MainScreen")

    def log_out(self):
        try:
            msg = self.channel.disconnect(self.username)
            self.session_active = False
            self.channel.api_server.stop()
        except Exception as e:
            self.log.error("Can't close session: %s", e)
        else:
            self.log.info("Logged out: %s", msg)
            logout = LogoutScreen()
            Window.size =  (INFO_WIDTH, INFO_HEIGTH)
            self.manager.switch_to(logout)

    def add_chat(self, req_channel, contact):
        chat = ChatScreen(header=self.header, channel=req_channel, stop=self.remove_chat, name=contact.username)
        # add screen
        self.ids.sm_chats.add_widget(chat)
        self.ids.sm_chats.current = contact.username
        # update active chats
        self.ids.chats_list.active.append(contact)
        # add to server
        self.channel.api_server.add_chat(contact)

        self.log.debug("Added chat with %s", contact)
        return chat

    def remove_chat(self, username):
        # unbind
        screen = self.ids.sm_chats.get_screen(username)
        screen.unbind(name=self.ids.sm_chats._screen_name_changed)
        screen.manager = None
        # remove
        self.ids.sm_chats.screens.remove(screen)
        self.ids.sm_chats.current = "default"
        # update active chats
        self.ids.chats_list.active.remove(username)
        # remove from server
        self.channel.api_server.remove_chat(username)

        self.log.debug("Removed chat with %s", username)

    def new_connection(self, contact):
        print("new conn")
        try:
            if self.ids.sm_chats.has_screen(contact.username):
                self.log.info("Already connected with %s", contact)
                return self.ids.sm_chats.get_screen(contact.username)

            req_channel = RequestChannel(contact.ip_address, contact.port)
            server = self.channel.api_server
            res = req_channel.new_connection(server.ip, server.port, self.username)
        except Exception as e:
            self.log.error("Can't create connection: %s", e)
        else:
            return self.add_chat(req_channel, contact)

    @mainthread
    def entry_connection(self, contact_username, contact_ip, contact_port):
        req_channel = RequestChannel(contact_ip, contact_port)
        return self.add_chat(req_channel, ContactItem(contact_username, contact_ip, contact_port))

    @mainthread
    def entry_message(self, username, ip_address, port, text):
        self.ids.sm_chats.current = username
        chat = self.ids.sm_chats.current_screen
        chat.draw_text_case(text, RECD)

    @mainthread
    def entry_audio_call(self, username, ip_address):
        screen = self.ids.sm_chats.get_screen(username)
        screen.open_audio_call()

class ChatScreen(Screen):
    def __init__(self, header, channel, stop, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        self.channel = channel
        self.header = header
        self.close_function = stop
        self.log = Logger.getFor("ChatScreen")

    def send(self, message):
        try:
            self.channel.send_text(self.header + message)
            self.draw_text_case(message, SEND)
        except Exception as err:
            self.log.error("Can't send message: %s", err)
            self.draw_text_case(message, NSEND)
        finally:
            self.ids.block_of_typos.text=''

    def close_chat(self):
        self.close_function(self.name)

    def video_call(self):
        pass

    def audio_call(self):
        try:
            # self.channel.begin_call(self.header + AUDIO)
        except Exception as e:
            self.log.error("Can't start call: %s", e)
        else:
            self.open_audio_call()

    def draw_text(self, text, color, halign):
        width = self.ids.messages.container.width - 10
        label = MyLabel(text=text, color=color, halign=halign, size=(width, None))
        self.ids.messages.adapter.data.append(label)

    def draw_text_case(self, text, type):
        if type == SEND:
            self.draw_text(text, RGB_SEND, 'right')
        elif type == RECD:
            self.draw_text(text, RGB_RECD, 'left')
        else:
            self.draw_text(text, RGB_NSEND, 'right')

    def open_audio_call(self):
        self.log.debug("Creating panel for audio_call")
        #x = AudioWidget(self.channel)
        #self.ids.actions_buttons.add_widget(x)
