# Redes2017

## Práctica 6

**Integrantes**

1. Coloapa Díaz Alejandra Krystel
2. Marín Arriaga Adolfo
3. Ochoa González Uriel A.

### Reporte

**1.** Si se tienen 3 clientes conectados al sistema que solo intercambian mensajes de texto y cada 20 segundos un cliente le responde a los 2 con los que se está hablando; sup cada mensaje ocupa 2 paquetes y los *ping* un paquete. ¿Porcentaje de tráfico que genera por conversación *vs* el porcentaje por las funcionalidades agregadas?

Tomemos como medida 60 segundos. Los *ping* s para las nueva funcinalidad se realizan cada 5 segundos => 12 peticiones en 60s => 12 paquetes.
Por otra parte, (asumiendo) cada cliente responde cada 20 segundos dos mensajes => 3 peticiones por cada mensaje => 6 paquetes, en total, 18 paquetes.

**En total**: 30 paquetes en 60s, de los cuales 40% es de *ping* s y 60% de la conversación.

**2.**. ¿Cuántos clientes intercambiando mensajes entre sí debe haber para que el porcentaje de tráfico sea mayor?

Suponiendo que cada cliente le contesta a *n* contactos conectados cada 30 segundos, entonces genera *2n* (n mensajes que ocupan 2 paquetes) paquetes mientras que hay 6 paquetes por funcionalidad.
Si cada cliente hace lo mismo, se tiene *2(n x n)*  (n veces el tráfico) paquetes; para que el porcentaje sea mayor, *n x n* debe ser mayor a 3.

Entonces, si todos los clientes se encuentran activos, basta con que haya 2 pues se tendrían *2(n x n) = 2(4) = 8 > 6* paquetes.

### Dependencias
* ``Python 3``
* ``Kivy >= v1.9``
* `` gi v1.2``
* ``PyAudio``


Uso:

* Para uso local

``$ python3 GraphicalUserInterface.py -- -l``

* Para uso remoto

``$ python3 GraphicalUserInterface.py --``

* Se debe levantar el servidor de contactos: ``$ cd Directory && python3 Directory.py``
