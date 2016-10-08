#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Format responses
def build_response(func):
    def format_response(*args):
        status, string_message = func(*args)
        return {STATUS: status, MESSAGE: string_message}
    return format_response

# Format querys
def decode_message(func):
    def format_message(self, message):
        message_split = split_message_header(message)
        contact_username =  message_split[MESSAGE_USERNAME]
        contact_ip = message_split[MESSAGE_IP]
        contact_port = message_split[MESSAGE_PORT]
        text_message = message_split[MESSAGE_TEXT]
        return func(self, contact_username, contact_ip, contact_port, text_message)
    return format_message

# interpreter for args when creating connections
def parse_params(func):
    def get_ip_address(self, contact_ip=None, contact_port=None):
        ip = contact_ip if contact_ip else get_ip_address()
        port = int(contact_port) if contact_port else CHAT_PORT
        return func(self, ip, port)
    return get_ip_address

# wrap request to a proxy
def try_catch(func):
    def wrap_request(self, *args):
        try:
            func(*args)
        except ProtocolError as e:
            self.log.error("Can't resolve request: %s", func.__name__)
            raise ConnectionAbortedError()
        else:
            self.log.info("Request completed")
    return wrap_request
