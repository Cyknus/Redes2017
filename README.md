# Redes2017

## Práctica 5

**Integrantes**

1. Coloapa Díaz Alejandra Krystel
2. Marín Arriaga Adolfo
3. Ochoa González Uriel A.

### Reporte

**1.- ¿Cuál es el principal problema de la arquitectura propuesta?**

Que cualquier persona podría hacerse pasar por cualquier usuario (si A ve el *username* de B, puede usarlo después como suyo). Además un usuario no tiene información persisente en la aplicación.

**2.- ¿Cómo solucionarías este problema? **

Creando un registro de usuarios para asignarles a cada uno un *username* único con el cuál puedan identificarse.

**3.- ¿Existe forma de saber de donde proviene el mensaje sin el encabezado? **

No, pues el servidor sólo está a la escucha y no sabe de donde recibe el mensaje.

**4.- Particularidades del código**
Se sigue usando Kivy y se refactoriza la división de la definición de las pantallas. La GUI es una mezcla extraña de apuntadores entre pantallas para poder mantener todo actualizado y acceder a componentes externas sin tener que pasar muchos parámetros en la creación. 

Se agregó un *Logger* con el fin de rastrear la comunicación entre usuarios. 

Falta la integración con Audio, pues hay que agregar una cadena de identificación a los bytes de streaming y Kivy no soporta la apertura de segundas ventanas.

### Dependencias
* Python 3
* Kivy 1.9

Uso:

* Para uso local

*python3 GraphicalUserInterface.py -- -l*

* Para uso remoto

*python3 GraphicalUserInterface.py --*
