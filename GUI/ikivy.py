#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from kivy.uix.label import Label
from kivy.adapters.models import SelectableDataItem
from kivy.adapters.simplelistadapter import SimpleListAdapter
from Constants.Constants import *

class MyLabel(Label):
    def __init__(self, text, color, size, halign, **kwargs):
        super(MyLabel, self).__init__(text=text,
            color=color,
            text_size=size,
            halign=halign,
            **kwargs)
        self.texture_update()
        self.size = self.width, self.texture_size[1]

class MyListAdapter(SimpleListAdapter):
    def __init__(self):
        super(MyListAdapter, self).__init__(data=[], cls=MyLabel, args_converter=lambda ri, o: {
            'text': o.text,
            'color': o.color,
            'size_hint': (1, None),
            'size': o.text_size,
            'halign': o.halign})

class ContactItem(SelectableDataItem):
    def __init__(self, username, ip_address, port, is_selected=False, **kwargs):
        super(ContactItem, self).__init__(**kwargs)
        self.username = username
        self.ip_address = ip_address
        self.port = port
        self.is_selected = is_selected

    def __str__(self):
        return self.username + " at " + self.ip_address + "@" + str(self.port)

    def __eq__(self, other):
        if type(other) is ContactItem:
            return other.username == self.username
        elif type(other) is str:
            return other == self.username
        return False
