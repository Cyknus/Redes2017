#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.listview import ListView, ListItemButton
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.modalview import ModalView
from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from .ikivy import *
from Constants.Constants import *
from Constants.AuxiliarFunctions import *
from Channel.DirectoryChannel import DirectoryChannel
from Channel.Channels import RequestChannel
from Channel.AudioCall import *
import multiprocessing as mp

Window.clearcolor = RGBA_BG
Builder.load_file('GUI/screens.kv')

class LoginManager(Screen):
    def doLogin(self, server_ip, server_port, my_port=None):
        try:
            print("[info] Linking to server at " + server_ip + "@" + server_port)
            directory = DirectoryChannel(self.manager, server_ip, server_port, my_port)
            connect = ConnectScreen(directory=directory, name="connect")
            self.manager.switch_to(connect)
        except OSError as err:
            print("[err] Can't raise locla server :: " + str(err))

class LocalLoginScreen(LoginManager):
    def accessRequest(self, my_port, server_address, server_port):
        print("[info] Raising local server in port " + my_port)
        self.doLogin(server_address, server_port, my_port)

class RemoteLoginScreen(LoginManager):
    def accessRequest(self, server_address, server_port):
        print("[info] Raising local server in default mode")
        self.doLogin(server_address, server_port)

class ConnectScreen(Screen):
    def __init__(self, directory, **kwargs):
        super(ConnectScreen, self).__init__(**kwargs)
        self.channel = directory

    def connect(self, username):
        try:
            dict_contacts = self.channel.connect(username)
            print("[info] Logged as " + username)
            main_app = MainScreen(username=username, channel=self.channel, name="main")
            main_app.ids.contacts_list.load_contacts(dict_contacts)
            Window.size = (MAIN_WIDTH, MAIN_HEIGHT)
            self.manager.switch_to(main_app)
        except Exception as e:
            print("[err] GUI :: An error occurred during connection: " + str(e))

class ContactsList(Screen):
    def __init__(self, **kwargs):
        super(ContactsList, self).__init__(**kwargs)
        # build adapter
        args_converter = lambda ri, o: {'text': o.username, 'size_hint_y': None, 'height': 25}
        adapter = ListAdapter(data=[],
                                    args_converter=args_converter,
                                    propagate_selection_to_data=True,
                                    cls=ListItemButton,
                                    selection_mode='single')
        adapter.bind(on_selection_change=self.new_chat)
        # create list
        contact_list = ListView(adapter=adapter)
        self.add_widget(contact_list)

        # pointer to adapter data
        self.data = adapter.data

    def new_chat(self, adapter, *args):
        if len(adapter.selection) == 0:
            return
        # get data item
        selected_contact = adapter.selection[0]
        selected_item_data = list(filter(lambda o: o.username == selected_contact.text, adapter.data))[0]
        # open message modal
        view = NewChatModal(self.top_parent, selected_item_data)
        view.open()

    def load_contacts(self, dict_contacts):
        for k,v in dict_contacts.items():
            self.data.append(ContactItem(v[NAME_CONTACT], v[IP_CONTACT], v[PORT_CONTACT]))

    def update_contacts(self):
        try:
            dict_contacts = self.top_parent.channel.get_contacts(self.top_parent.username)
            not_online = filter(lambda o: o.username not in dict_contacts, self.data)
            # drop old
            for v in not_online:
                self.data.remove(v)
            # add news
            new_online = {k:v for k, v in dict_contacts.items() if k not in self.data}
            for k,v in new_online.items():
                self.data.append(ContactItem(v[NAME_CONTACT], v[IP_CONTACT], v[PORT_CONTACT]))
        except Exception as e:
            print("[err] GUI :: An error occurred during updating contacts" + str(e))

class NewChatModal(ModalView):
    def __init__(self, chats_screen, contact, **kwargs):
        super(NewChatModal, self).__init__(**kwargs)
        self.chats_screen = chats_screen
        self.to_contact = contact
        self.ids.contact_username.text = "Nuevo Mensaje:\n" + self.to_contact.username

    def send_message(self, message):
        chat = self.chats_screen.new_connection(self.to_contact)
        chat.send(message)
        self.dismiss()

class ChatsActiveList(Screen):
    def __init__(self, **kwargs):
        super(ChatsActiveList, self).__init__(**kwargs)
        # build adapter
        args_converter = lambda ri, o: {'text': o.username, 'size_hint_y': None, 'height': 50}
        adapter = ListAdapter(data=[],
                                    args_converter=args_converter,
                                    propagate_selection_to_data=True,
                                    cls=ListItemButton,
                                    selection_mode='single')
        adapter.bind(on_selection_change=self.open_chat)
        # create list
        contact_list = ListView(adapter=adapter)
        self.add_widget(contact_list)

        # pointer to list
        self.active = adapter.data

    def open_chat(self, adapter, *args):
        if len(adapter.selection) == 0:
            return

        selected_contact = adapter.selection[0]
        self.sm.current = selected_contact.text

class MainScreen(Screen):
    def __init__(self, channel, username, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.channel = channel
        self.username = username
        self.session_active = True

    def log_out(self):
        try:
            msg = self.channel.disconnect(self.username)
            self.session_active = False
            self.channel.api_server.stop()
            print("[info] " + msg)
            logout = LogoutScreen()
            self.manager.switch_to(logout)
            Window.size =  (INFO_WIDTH, INFO_HEIGTH)
        except Exception as e:
            print("[err] An error occurred when logging out :: " + str(e))

    def add_chat(self, req_channel, contact):
        header = get_message_header(self.username, self.channel.api_server.ip)
        chat = ChatScreen(header=header, channel=req_channel, stop=self.remove_chat, name=contact.username)
        self.ids.sm_chats.add_widget(chat)
        self.ids.sm_chats.current = contact.username
        self.ids.chats_list.active.append(contact)
        return chat

    def remove_chat(self, username):
        print("[info] closing chat with " + username)
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

    def new_connection(self, contact):
        try:
            print("[info] connecting with " + contact.username)
            if self.ids.sm_chats.has_screen(contact.username):
                print("[info] already connected")
                return self.ids.sm_chats.get_screen(contact.username)

            req_channel = RequestChannel(contact.ip_address, contact.port)
            server = self.channel.api_server
            res = req_channel.new_connection(server.ip, server.port, self.username)
            print("[info] " + contact.username + " response: " + res)
            self.channel.api_server.chats_dictionary[contact.username] = contact.ip_address
            return self.add_chat(req_channel, contact)
        except Exception as e:
            print("[err] An error occurred when creating chat :: " + str(e))

    @mainthread
    def entry_connection(self, contact_username, contact_ip, contact_port):
        print("[info] Creating chat with " + contact_username)
        req_channel = RequestChannel(contact_ip, contact_port)
        print("[info] Adding screen..")
        return self.add_chat(req_channel, ContactItem(contact_username, contact_ip, contact_port))

    @mainthread
    def entry_message(self, username, ip_address, text):
        self.ids.sm_chats.current = username
        chat = self.ids.sm_chats.current_screen
        chat.draw_text_case(text, RECD)

    @mainthread
    def entry_audio_call(self, username, ip_address):
        print("[info] Creating streams")
        screen = self.ids.sm_chats.get_screen(username)
        screen.open_audio_call()

class LogoutScreen(Screen):
    pass

class ChatScreen(Screen):
    def __init__(self, header, channel, stop, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        self.channel = channel
        self.header = header
        self.close_function = stop

    def send(self, message):
        try:
            self.channel.send_text(self.header + message)
            self.draw_text_case(message, SEND)
        except Exception as err:
            print("[err] When sending message :: " + str(err))
            self.draw_text_case(message, NSEND)
        self.ids.block_of_typos.text=''

    def close_chat(self):
        self.close_function(self.name)

    def video_call(self):
        pass

    def audio_call(self):
        try:
            res = self.channel.begin_call(self.header + AUDIO)
            print("Contact response " + res)
            self.open_audio_call()
        except Exception as e:
            print(e)
            print("Can't create call")

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
        print("opening panel..")
        x = AudioWidget(self.channel)
        self.ids.actions_buttons.add_widget(x)

class AudioWidget(BoxLayout):
    def __init__(self, channel, **kwargs):
        super(AudioWidget, self).__init__(**kwargs)
        # self.pa_call = AudioCall()
        # self.pa_call.openOutput()
        # self.pa_call.record(self.callback_audio)
        self.channel = channel

    def hang_up(self):
        # self.pa_call.stopOutput()
        # self.pa_call.stop()
        self.parent.remove_widget(self)

    def callback_audio(self, in_data, f, t, s):
        self.channel.send_bytes(in_data)
        return (None, AudioCall.CONTINUE)

    @mainthread
    def play_audio(self, audio):
        self.pa_call.play(audio)

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
        Window.size = (LOGIN_WIDTH, LOGIN_HEIGTH)

    def build(self):
        return self.sm

    def on_stop(self):
        print("[debug] Leaving..")
        screen = self.sm.current_screen
        c_class = type(screen)

        if c_class is MainScreen and screen.session_active:
            print("[info] Logging out..")
            screen.log_out()
        elif c_class is ConnectScreen:
            print("[info] Shutting down server..")
            screen.channel.api_server.stop()
