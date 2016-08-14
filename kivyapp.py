import kivy
kivy.require('1.9.1')

from kivy.app import App 
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput 
from kivy.uix.button import Button 
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen


class LoginScreen(GridLayout):


    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.sm = ScreenManager()
        self.screen = Screen(name='login')
        self.sm.add_widget(self.screen)
        self.screen = Screen(name='calcu')
        self.sm.add_widget(self.screen)
        self.cols = 2
        self.btn = Button(text="ingresar")
        self.username = TextInput(multiline=False)
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(Label(text='login'))
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.add_widget(self.password)
        self.add_widget(self.btn)
        self.btn.bind(on_press=self.btnPressed)

    def btnPressed(self, btn):
        authorized = self.validate(self.username.text, self.password.text)
        if authorized:
            self.sm.current = 'calcu'
        else:
            popup = Popup(title='Error de login', 
                content=Label(text="No tienes acceso al sistema."),
                size=(300,100),
                size_hint=(None, None))
            popup.open()

    def validate(self, username, password):
        return username == "hola" and password == "mundo"

class MyApp(App):
    """docstring for MyApp"""
    
    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    MyApp().run()