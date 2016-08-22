#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from kivy.uix.label import Label
from Constants import *

# better label
class MyLabel(Label):
    def __init__(self, text, color):
        super(MyLabel, self).__init__(text=text, color=color)
        self.size_hint = Constants.SIZE_HINT_MSG
        self.height = Constants.MSG_HEIGHT
        self.width = Constants.CHAT_SIZE[0] - 10
        # self.text_size = self.size
