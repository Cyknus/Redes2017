# Redes2017

## Ejercicio 1

**Integrantes**

1. Coloapa Díaz Alejandra Krystel
2. Marín Arriaga Adolfo
3. Ochoa González Uriel A.

### Reporte

**1. Funcionalidad de pcap**
*pcap* es un protocolo de comunicación de internet que permite a una computadora/dispositivo recibir paquetes de la red. Esencialmente convierte información digital en señales (paquetes) usando un algoritmo específico, estas señales son recibidas por otra computadora y procesadas. Puede ser usado como un protocolo de análisis, monitor de red, generador de tráfico..

**2. Vulnerabilidades del protocolo HTTP**
No está encriptado y es vulnerable a ataques *man-in-the-middle* y *eavesdropping* que pueden dar acceso al sitio e información delicada a los atacantes, con ello pueden modificar el contenido e insertar malware. Por otra parte, tampoco valida los dominios.

**3. Ataques**
- Network eavesdropping. Ataque a la capa de red que se centra en capturar paquetes transmitidos por otras computadoras y leer la información contenida con fin de buscar cierto tipo de datos. Este ataque es común por la falta de servicios de encriptación.
- man-in-the-middle. El atacante en secreto altera la comunicación entre dos partes que creen comunicarse directamente entre ellas. 

**4. Código**
Se uso la función *pcap_loop* para capturar paquetes indefinidamente, por cada uno que se captura se decodifican los encabezados de cada capa y se obtiene el *payload*, el mensaje transmitido. Para obtener los mensajes de HTTP se usa el filtro "tcp port 80" (pues es el estándar). 

Al programa le falta la funcionalidad de guardar en archivo y filtrar sólo los campos requeridos, por ello por cada paquete que se recibe sólo se imprime en consola.

### Dependencias
* gcc
* libpcap
