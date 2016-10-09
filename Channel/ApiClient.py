#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from xmlrpc.client import ServerProxy
from Services.Decorators import parse_params


class MyApiClient:
    @parse_params
    def __init__(self, contact_ip=None, contact_port=None):
        self.proxy = ServerProxy('http://%s:%i'%(contact_ip, int(contact_port)), allow_none=True)
