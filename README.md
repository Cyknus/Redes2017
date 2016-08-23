# Redes2017

Práctica 2

### Reporte

**1.- Definir el concepto de procedimientos remotos**

Consisten en un protocolo que permite a un software o programa ejecutar código en otra máquina remota sin preocuparse por la comunicación ocultando todos los detalles del código correspondiente a la comunicación a través de la red.

**2.- ¿Qué es una IP y para qué sirve?**

El protocolo de internet (Internet Protocol) es un protocolo de comunicación de datos digitales clasificado funcionalmente en la capa de red (capa que proporciona conectividad y selección de ruta entre dos sistemas de hosts que pueden estar ubicados en redes geográficamente distintas.)
Es utilizado para la comunicación de datos a través de una red de paquetes combinados.

**3.- ¿Qué es un puerto?**

Éste especifica la aplicación a la que se dirigen los datos, así, cuando el equipo recibe información que va dirigida a un puerto, los datos se envían a la aplicación relacionada. Si se trata de una solicitud enviada a la aplicación, la aplicación se denomina aplicación servidor. Si se trata de una respuesta, entonces hablamos de una aplicación cliente.

**4.- ¿Se puede tener dos clientes en una misma computadora?**
Sí

**5.- Particularidades del código**
* Flujo del problema.
  En la carpeta GUI sólo se tienen los archivos referentes a la especificación de las pantallas.
  El archivo *Chat.py* contiene la definición de los controladores de las interfaces, se definen los métodos para responder ante los eventos de conexión y envío de mensajes. Para ello, se tiene asociada una instancia de *MyApiClient* que a su vez maneja una instancia de *Channel* a través de la cuál se manejan las conexiones.
  *MyApiClient* sirve como intermedio entre la GUI y el servidor local, a través de él se realizan los diferentes procesos mientras que *MyApiServer* sólo define las funciones disponibles para el contacto.
* Principales problemas que se encontraron y cómo los solucionaron
  Principalmente fue el manejo de la estructura de clases dada, pues no hallábamos como interconectar las piezas. (Para ello seguimos la documentación y envíamos correos)
* Problemas que no fueron solucionados.
  En la GUI.. los mensajes enviados no tienen el formato que esperábamos. En general, nos apegamos  a la documentación e implementamos los métodos de forma que (al menos para nosotros) tuviera sentido.

### Dependencias
* Python 3
* Kivy 1.9

Uso:

*python3 GraphicalUserInterface.py -- -l* Para uso local
*python3 GraphicalUserInterface.py --* Para uso en distintos equipos
