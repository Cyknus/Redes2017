# Redes2017

## Práctica 3

**Integrantes**

1. Coloapa Díaz Alejandra Krystel
2. Marín Arriaga Adolfo
3. Ochoa González Uriel A.

### Reporte

**1.- ¿Si le pasas el proyecto a alguien que se encuentre al otro lado del mundo, podrían comunicarse?**

Siempre y cuando las computadoras tengan acceso remoto entre ellas, podrían comunicarse

**2.- ¿Bajo que restricciones podrían comunicarse?**

Cuando ambas tienen una IP fija a la cuál contactar (de otro modo, está enmascarada bajo la red local y no podrían conectarse entre ellas)

**3.-**

Se pueden comunicar pues están en la misma red local.. se asignan IP bajo el módem y podrían entablar comunicación; para poder comunicarse tendrían que estar conectados a la misma red (o se vuelve el caso anterior)

**4.- Particularidades del código**
* Flujo del problema.
  Se mantuvieron las definiciones de clase de la práctica 2, agregando al server la función para manejar la entrada del audio. Se crea la clase *AudioCall* para manejar una sola instancia de pyAudio.

  Un problema fue la sincronización de los hilos, pues al grabar se envían los bytes continuamente (y si se reproducen ahí mismo, la comunicación es perfecta) sin embargo, al enviarlos por la red el servidor de alguna forma tiene que reproducir esos bytes (pero está en otro hilo) lo que nos ocasionó problemas pues no reproducía bien la llamada. (Problema sigue sin resolverse por completo).

  Por otra parte, para que al recibir audio el contacto pueda reproducirlo, se tiene que tener el *stream* abierto.. pero tendría que haber notificación de que debe abrirse (al abrir y cerrarlo a cada llamada, dejaba de reproducir y si no se cierra, eventualmente hay una excepción). La solución temporal fue dejar el *stream* abierto desde el inicio y cerrarlo al finalizar la aplicación.

  Al botón de llamada en lugar de lanzar otra pantalla, se actualiza con la opción de colgar.

### Dependencias
* Python 3
* Kivy 1.9

Es necesario instalar todas las dependencias de fuentes (pip install kivy) debería funcionar.

Uso:

* Para uso local

*python3 GraphicalUserInterface.py -- -l*

* Para uso remoto

*python3 GraphicalUserInterface.py --*
