from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

import json

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<LoginScreen>:
    GridLayout:
        cols:
            2
        Label:
            text: 'Usuario'
        TextInput:
            id: username
            text: 'hola'
            multiline: False
        Label:
            text: 'Password'
        TextInput:
            id: password
            multiline: False
            text: 'mundo'
            password: True
        Button:
            text: 'Ingresar'
            on_press: root.accessRequest(username.text, password.text)
        Button:
            text: 'Limpiar'
            on_press: username.text=''
            on_press: password.text=''

<UserAddScreen>:
    GridLayout:
        cols:
            2
        Label:
            text: 'Usuario'
        TextInput:
            id: nusername
            multiline: False
        Label:
            text: 'Password'
        TextInput:
            id: npassword
            multiline: False
            password: True
        Button:
            text: 'Agregar usuario'
            on_press: root.userAdd(nusername.text, npassword.text)
        Button:
            text: 'Limpiar'
            on_press: nusername.text=''
            on_press: npassword.text=''

<CalculatorScreen>:
    FloatLayout:
        Label:
            id: display
            text: ''
            text_size: self.size
            halign: 'right'
            valign: 'middle'
            size_hint: .95,.20
            pos_hint: {'x':0, 'y':.81}

        Button:
            id: number0
            text: '0'
            size_hint: .20,.20
            pos_hint: {'x': .20, 'y':0}
            on_press: root.showOnDisplay('0')
        Button:
            id: number1
            text: '1'
            size_hint: .20,.20
            pos_hint: {'x': 0, 'y':.20}
            on_press: root.showOnDisplay('1')
        Button:
            id: number2
            text: '2'
            size_hint: .20,.20
            pos_hint: {'x': .20, 'y':.20}
            on_press: root.showOnDisplay('2')
        Button:
            id: number3
            text: '3'
            size_hint: .20,.20
            pos_hint: {'x': .40, 'y':.20}
            on_press: root.showOnDisplay('3')
        Button:
            id: number4
            text: '4'
            size_hint: .20,.20
            pos_hint: {'x': .0, 'y':.40}
            on_press: root.showOnDisplay('4')
        Button:
            id: number5
            text: '5'
            size_hint: .20,.20
            pos_hint: {'x': .20, 'y':.40}
            on_press: root.showOnDisplay('5')
        Button:
            id: number6
            text: '6'
            size_hint: .20,.20
            pos_hint: {'x': .40, 'y':.40}
            on_press: root.showOnDisplay('6')
        Button:
            id: number7
            text: '7'
            size_hint: .20,.20
            pos_hint: {'x': 0, 'y':.60}
            on_press: root.showOnDisplay('7')
        Button:
            id: number8
            text: '8'
            size_hint: .20,.20
            pos_hint: {'x': .20, 'y':.60}
            on_press: root.showOnDisplay('8')
        Button:
            id: number9
            text: '9'
            size_hint: .20,.20
            pos_hint: {'x': .40, 'y':.60}
            on_press: root.showOnDisplay('9')
        Button:
            size_hint: .20,.20
            pos_hint: {'x':.40, 'y':0}
            text: 'limpiar'
            on_press: display.text=''


        Button:
            size_hint: .20,.20
            pos_hint: {'x':0, 'y':0}
            text: '+'
            on_press: root.showOnDisplay('+')
        Button:
            size_hint: .20,.20
            pos_hint: {'x':.40, 'y':0}
            text: '-'
            on_press: root.showOnDisplay('-')
        Button:
            size_hint: .20,.20
            pos_hint: {'x':.60, 'y':0}
            text: '*'
            on_press: root.showOnDisplay('*')
        Button:
            size_hint: .20,.20
            pos_hint: {'x':.60, 'y':.20}
            text: '/'
            on_press: root.showOnDisplay('/')
        Button:
            size_hint: .20,.20
            pos_hint: {'x':.60, 'y':.40}
            text: '%'
            on_press: root.showOnDisplay('%')
        Button:
            size_hint: .20,.20
            pos_hint: {'x':.60, 'y':.60}
            text: '**'
            on_press: root.showOnDisplay('**')
        Button:
            size_hint: .20,.40
            pos_hint: {'x':.80, 'y':0}
            text: '='
            on_press: root.showOnDisplay(display.text,True)

        Button:
            size_hint: .20,.40
            pos_hint: {'x':.80, 'y':.40}
            text: 'agrega usuario'
            on_press: root.userAddRequest()

""")


# Declare both screens
    
class LoginScreen(Screen):
    def accessRequest(self, username, password):
        authorized = self.validate(username, password)
        if authorized:
            self.ids.password.text = ''
            sm.current = 'calculator'
        else:
            popup = Popup(title='Error de login', 
                content=Label(text="No tienes acceso al sistema."),
                size=(300,100),
                size_hint=(None, None))
            popup.open()

    def validate(self, username, password):
        encrypted = self.encryptPassword(password)
        users = json.load(open("input.txt"))
        for i in users:
            if i == username:
                return users[i] == encrypted
        return False

    @staticmethod
    def encryptPassword(password):
        cipher = ''
        for c in password:
            cipher += chr(ord(c)+5)
        return cipher


class CalculatorScreen(Screen):
    def showOnDisplay(self, text, evaluate=False):
        if evaluate:
            self.ids.display.text = str(float(eval(text)))
        else:
            self.ids.display.text += text
    def userAddRequest(self):
        sm.current = 'user'

class UserAddScreen(Screen):
    """docstring for UserAddScreen"""
    def userAdd(self, user, password):
        users = json.load(open("input.txt"))        
        
        if user == '' or password == '':
            popup = Popup(title='Error', 
                content=Label(text="No pueden ser campos vacíos."),
                size=(300,100),
                size_hint=(None, None))
            popup.open()
        if user in users:
            popup = Popup(title='Error', 
                content=Label(text="Ese nombre ya existe, intenta otro."),
                size=(300,100),
                size_hint=(None, None))
            popup.open()
            self.clean()
        else:
            users[user] = LoginScreen.encryptPassword(password)
            json.dump(users, open("input.txt", 'w'))
            self.clean()
            sm.current = 'login'

    def clean(self):
            self.ids.npassword.text = ''
            self.ids.nusername.text = ''
        

# Create the screen manager
sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(CalculatorScreen(name='calculator'))
sm.add_widget(UserAddScreen(name='user'))

class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()