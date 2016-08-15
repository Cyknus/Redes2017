from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from Code.ScientificCalculator import ScientificCalculator

import json

# Carga el archivo que tiene la descripción de las ventanas.
Builder.load_file('GUI/screens.kv')

# Declara la primera vista que será la del login.

class LoginScreen(Screen):
    """ Clase que describe las acciones disponibles en la pantalla de acceso
    """

    def accessRequest(self, username, password):
        """Petición de acceso a la calculadora.

        Keyword arguments:
        username -- el nombre de usuario
        password -- contraseña del usuario
        """
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
        """Busca en la base de datos el nombre de usuario y cifra la contraseña
        para verificar que el usuario tiene permiso.

        Keyword arguments:
        username -- el nombre de usuario
        password -- contraseña del usuario
        """
        encrypted = self.encryptPassword(password)
        users = json.load(open("Code/input.txt"))
        if username in users:
            return users[username] == encrypted
        return False

    @staticmethod
    def encryptPassword(password):
        """Cifra la contraseña sumando 5 unidades al código ascii de cada carac-
        ter de la contraseña. Es estático porque porqué no.

        Keyword arguments:
        password -- la contraseña que será cifrada.
        """
        cipher = ''
        for c in password:
            cipher += chr(ord(c)+5)
        return cipher


class CalculatorScreen(Screen):
    """ Clase que describe las acciones disponibles en la pantalla de la 
    calculadora
    """
    newOp = False # Bandera para indentificar nuevas operaciones.
    cal = ScientificCalculator() # Calculadora para las operaciones.

    def showOnDisplay(self, text, evaluate=False):
        """Modifica lo que es visto en el display de la calculadora.

        Keyword arguments:
        text -- el texto que se encuentra en este momento en el display.
        evaluate -- permanece falso a menos que el boton de "=" sea presionado. 
        """
        if evaluate:
            self.newOp = True
            self.ids.display.text = str(self.cal.evaluate(text))
        else:
            if self.newOp:
                self.ids.display.text = text
                self.newOp = False
            else:
                self.ids.display.text += text
    def userAddRequest(self):
        """Cuando el boton de agregar usuario sea presionado cambia la pantalla
        """
        sm.current = 'user'

class UserAddScreen(Screen):
    """ Clase que describe las acciones disponibles en la pantalla para agregar
    usuarios
    """
    def userAdd(self, user, password):
        """Agrega un usuario a la base de datos, verificando que los campos no 
        sean vacíos y que el nombre de usuario no exista ya.

        Keyword arguments:
        user -- el nombre de usuario que se desea agregar a la base.
        password -- contraseña asociada al usuario que se desea agregar a la base.
        """
        users = json.load(open("Code/input.txt"))        
        
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
            json.dump(users, open("Code/input.txt", 'w'))
            self.clean()
            sm.current = 'login'

    def clean(self):
        """Si lo haces más de una vez, crea una rutina. Solo limpia los campos
        de nombre y password en esta pantalla
        """
        self.ids.npassword.text = ''
        self.ids.nusername.text = ''
        

# Crea el screenmanager y las pantallas (cosas de kivy)
sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(CalculatorScreen(name='calculator'))
sm.add_widget(UserAddScreen(name='user'))

class CalculatorApp(App):
    """ Clase que echa a andar esta cosa."""
    def build(self):
        return sm

