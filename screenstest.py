from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<LoginScreen>:
    GridLayout:
        cols:
            2
        Label:
            text: 'Username'
        TextInput:
            multiline: False
        Label:
            text: 'Password'
        TextInput:
            multiline: False
            password: True
        Button:
            text: 'ingresar'
            on_press: root.imprimele()

<SettingsScreen>:
    BoxLayout:
        Button:
            text: 'My settings button'
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
""")

# Declare both screens
    
class LoginScreen(Screen):
    def imprimele(self):
        print('ok')

class SettingsScreen(Screen):
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(LoginScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))

class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()