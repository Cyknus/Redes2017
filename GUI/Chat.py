#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from .ikivy import MyLabel

from Channel.ApiClient import MyApiClient
from Channel.Channel import Channel

from Constants import *

from Channel.AudioCall import *

Window.clearcolor = Constants.RGBA_BG

# Descripción de las ventanas
Builder.load_file('GUI/screens.kv')
# Para manejar las pantallas
sm = ScreenManager()
# El cliente que se levanta
client = MyApiClient()
channel = Channel()
# Sólo una instancia de pyAudio
pa = AudioCall()
pa.openOutput() # TODO modularizar esto para no tener el stream abierto todo el tiempo.. => se mueve a otra pantalla

class LocalLoginScreen(Screen):
    def accessRequest(self, my_port, contact_port):
        """ Ingreso de modo local """
        print("Estableciendo conexión..")
        try:
            channel.connect_to(contact_port=contact_port)
            channel.server_up(client, my_port)
            print("Conexión establecida entre " + str(my_port) + " hacia " + str(contact_port))

            # lanzar la siguiente ventana
            sm.current = "chat"
            Window.size = Constants.CHAT_SIZE
        except Exception as e:
            if channel.server is not None:
                channel.server_down()
            print("No se ha podido establecer una conexión. Intenta de nuevo.")

class RemoteLoginScreen(Screen):
    def accessRequest(self, contact_ip):
        """ Ingreso de modo remoto """
        try:
            channel.connect_to(contact_ip=contact_ip)
            channel.server_up(client)
            print("Conexión establecida hacia " + str(contact_ip))

	        # lanzar la siguiente ventana
            sm.current = "chat"
            Window.size = Constants.CHAT_SIZE
        except Exception as e:
            if channel.server is not None:
                channel.server_down()
            print("No se ha podido establecer una conexión. Intenta de nuevo")

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        self.stream_record = None

    def send(self, text):
        if text == '':
            return

        try:
            channel.send_text(text)
            # aquí tiene que aparecer en pantalla el último enviado
            msg = MyLabel(text=text, color=Constants.RGB_SEND)
        except Exception as e:
            msg = MyLabel(text=text, color=Constants.RGB_NSEND)
            print("Mensaje no ha podido ser enviado.")

        client.display.add_widget(msg)
        # limpiar lo que está escrito
        self.ids.block_of_typos.text = ''

    def call(self):
        if self.stream_record is None:
            print("Llamando..")
            self.ids.call_button.text = 'Colgar'
            # abre el stream para grabar e inicia el thread que lo maneja
            self.stream_record = pa.record(callback)
        else:
            print("Colgando..")
            self.ids.call_button.text = "Llamar"
            # detener el servicio de llamada
            self.stream_record.stop()
            # Actualizar bandera
            self.stream_record = None

# mientras vemos a donde moverla..
def callback(in_data, f, t, s):
    channel.send_bytes(in_data) # TODO mandarlo a otro hilo, se está rezagando el cómo llegan los datos

    return (None, AudioCall.CONTINUE) # continuar grabando

# dummy class
class ChatApp(App):
    def build(self):
        return sm

    def on_stop(self):
        pa.closeOutput()
        if channel.server is not None:
            channel.server_down()

# acoplar todo
def build_screen_manager(local):
    if local:
        sm.add_widget(LocalLoginScreen(name="login"))
        size = Constants.SIZE_LL
    else:
        sm.add_widget(RemoteLoginScreen(name="login"))
        size = Constants.SIZE_RL

    Window.size = size # tamaño de acuerdo al login
    # set scroll view
    root = ChatScreen(name="chat")
    sm.add_widget(root)

    # Make sure the height is such that there is something to scroll.
    root.ids.layout.bind(minimum_height=root.ids.layout.setter('height'))
    client.display = root
    client.stream = pa.stream

    # creamos la aplicación
    chat = ChatApp()

    return chat
