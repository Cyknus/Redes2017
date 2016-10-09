#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .ikivy import *
from Channel.AudioCall import *
from Constants.Constants import *
from kivy.adapters.listadapter import ListAdapter
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen
from Services.Logger import *

Builder.load_file('GUI/kivy/chat_utils.kv')

class AudioWidget(BoxLayout):
    def __init__(self, channel, **kwargs):
        super(AudioWidget, self).__init__(**kwargs)
        # self.pa_call = AudioCall()
        # self.pa_call.openOutput()
        # self.pa_call.record(self.callback_audio)
        self.channel = channel
        self.log = Logger.getFor("AudioWidget")

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

# dummy class to create log out message screen
class LogoutScreen(Screen):
    pass

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

        # class logger
        self.log = Logger.getFor("ContactsList")

    def new_chat(self, adapter, *args):
        if len(adapter.selection) == 0:
            return

        # get data item
        selected_contact = adapter.selection[0]
        selected_item_data = list(filter(lambda o: o.username == selected_contact.text, adapter.data))[0]
        self.log.debug("New chat binding: %s", selected_item_data)
        # open message modal
        view = NewChatModal(self.top_parent, selected_item_data)
        view.open()

    def load_contacts(self, dict_contacts):
        contacts = dict_contacts.items()
        for k,v in contacts:
            self.data.append(ContactItem(v[NAME_CONTACT], v[IP_CONTACT], v[PORT_CONTACT]))
        self.log.info("%d contacts loaded", len(contacts))

    def update_contacts(self):
        try:
            dict_contacts = self.top_parent.channel.get_contacts(self.top_parent.username)
            not_online = list(filter(lambda o: o.username not in dict_contacts, self.data))
            self.log.debug("%d contacts droped", len(not_online))
            # drop old
            for v in not_online:
                self.data.remove(v)
            # add news
            new_online = {k:v for k, v in dict_contacts.items() if k not in self.data}
            self.log.debug("%d contacts added", len(new_online))
            for k,v in new_online.items():
                self.data.append(ContactItem(v[NAME_CONTACT], v[IP_CONTACT], v[PORT_CONTACT]))
        except Exception as e:
            self.log.error("Can't update contacts: %s", e)
        else:
            self.log.info("Contacts list updated")

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
