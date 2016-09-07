#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import mainthread
from .ikivy import MyLabel

from Channel.Channel import Channel
from Constants.Constants import *
from Constants import *
from Channel.AudioCall import *

Window.clearcolor = Constants.RGBA_BG

# Descripción de las ventanas
Builder.load_file('GUI/screens.kv')
# Instanciar manejador..
pa = AudioCall()
pa.openOutput() # TODO modularizar esto para no tener el stream abierto todo el tiempo.. => se mueve a otra pantalla

class LocalLoginScreen(Screen):
    def accessRequest(self, my_port, contact_port):
        """ Ingreso de modo local """
        print("Estableciendo conexión..")
        try:
            channel = Channel(gui=self.manager, my_port=my_port, contact_port=contact_port)
            print("Conexión establecida entre " + str(my_port) + " hacia " + str(contact_port))

            # lanzar la siguiente ventana
            chat = ChatScreen(channel=channel, name="chat")
            self.manager.switch_to(chat)
            Window.size = CHAT_SIZE
        except Exception as e:
            print("No se ha podido establecer una conexión. Intenta de nuevo.")

class RemoteLoginScreen(Screen):
    def accessRequest(self, contact_ip):
        """ Ingreso de modo remoto """
        try:
            channel = Channel(gui=self.manager, contact_ip=contact_ip)
            print("Conexión establecida hacia " + str(contact_ip))

	        # lanzar la siguiente ventana
            chat = ChatScreen(channel=channel, name="chat")
            self.manager.switch_to(chat)
            Window.size = CHAT_SIZE
        except Exception as e:
            print("No se ha podido establecer una conexión. Intenta de nuevo")

class ChatScreen(Screen):
    def __init__(self, channel, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        self.ids.layout.bind(minimum_height=self.ids.layout.setter('height'))
        self.channel = channel
        self.stream_record = None

    def send(self, text):
        if text == '':
            return

        try:
            self.channel.send_text(text)
            # aquí tiene que aparecer en pantalla el último enviado
            msg = MyLabel(text=text, color=RGB_SEND)
        except Exception as e:
            print(e)
            print("Mensaje no ha podido ser enviado.")
            msg = MyLabel(text=text, color=RGB_NSEND)

        self.ids.layout.add_widget(msg)
        # limpiar lo que está escrito
        self.ids.block_of_typos.text = ''

    @mainthread
    def display_message(self, text):
        msg = MyLabel(text=text, color=RGB_RECD)
        self.ids.layout.add_widget(msg)

    def call(self):
        if self.stream_record is None:
            print("Llamando..")
            self.ids.call_button.text = 'Colgar'
            # abre el stream para grabar e inicia el thread que lo maneja
            self.stream_record = pa.record(ChatScreen.callback)
            # abrir stream para escuchar
            #AudioCall.openOutput()
        else:
            print("Colgando..")
            self.ids.call_button.text = "Llamar"
            # detener el servicio de llamada
            self.stream_record.stop()
            # Actualizar bandera
            self.stream_record = None

    def play(self, audio):
        pa.openOutput()
        pa.stream.write(audio)
        pa.closeOutput()

    @staticmethod
    def callback(in_data, f, t, s):
        try:
            client.channel.send_bytes(in_data)
        except Exception as e:
            print(e)
            print("No se ha podido enviar audio")
        return (None, AudioCall.CONTINUE)

class ChatApp(App):
    def __init__(self, local_mode, **kwargs):
        super(ChatApp, self).__init__(**kwargs)
        self.sm = ScreenManager()
        if local_mode:
            self.sm.add_widget(LocalLoginScreen(name="login"))
            size = SIZE_LL
        else:
            self.sm.add_widget(RemoteLoginScreen(name="login"))
            size = SIZE_RL
        Window.size = size

    def build(self):
        return self.sm

    def on_stop(self):
        screen = self.sm.current_screen
        if type(screen) is ChatScreen:
            screen.channel.api_server.stop()
        pa.closeOutput()
