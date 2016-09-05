/*
*@file ejercicio1
*@brief Programa que permite capturar paquetes (1+) y analizarlos
*/

 #include <stdio.h>
 #include <stdlib.h>
 #include <pcap.h>
 #include <string.h>
 #include <ctype.h>
 #include <arpa/inet.h>
 #include "pcap.h"

/* Imprime el mensaje HTTP */
 void print_payload(const u_char *payload, int len)
 {
   /* ascii (if printable) */
  	const u_char *ch = payload;
    int i;
  	for(i = 0; i < len; i++) {
  		if (isprint(*ch))
  			printf("%c", *ch);
  		else
  			printf(".");
  		ch++;
  	}

    printf("\n");
 }

/* Procesa un paquete interceptado */
void callback(u_char *useless, const struct pcap_pkthdr *h, const u_char *p)
{
  static int count = 1;

  if(p != NULL) {
    const struct sniff_ethernet *ethernet;
    const struct sniff_ip *ip;
    const struct sniff_tcp *tcp;
    const char *payload;

    u_int size_ip;
    u_int size_tcp;
    u_int size_payload;

    /* Desarmar todos los encabezados */
    ethernet = (struct sniff_ethernet*) p;
    ip = (struct sniff_ip*) (p + SIZE_ETHERNET);
    size_ip = IP_HL(ip)*4;
    tcp = (struct sniff_tcp*)(p + SIZE_ETHERNET + size_ip);
    size_tcp = TH_OFF(tcp)*4;
    payload = (u_char *)(p + SIZE_ETHERNET + size_ip + size_tcp);
    size_payload = ntohs(ip->ip_len) - (size_ip + size_tcp);

    // el mensaje..
	  if (size_payload > 0) {
      printf("   Payload (%d bytes):\n", size_payload);
		  print_payload(payload, size_payload);
	  }
  }

  count++;
}

int sniff (char* device_name)
{
     char errbuf[PCAP_ERRBUF_SIZE];

     printf("Capturaremos del dispositivo: %s \n", device_name);
     pcap_t *captura = pcap_open_live(device_name, BUFSIZ, 1, -1, errbuf);

     if(captura== NULL) {
         printf("(ERROR) Captura: %s\n", errbuf);
         return EXIT_FAILURE;
     }

     struct bpf_program fp;
     bpf_u_int32 mask;
     bpf_u_int32 net;
     pcap_lookupnet(device_name, &net, &mask, errbuf);

     /* HTTP uses TCP:80 */
     if(pcap_compile(captura, &fp, "tcp port 80", 0, net) == -1) {
       printf("(ERROR) Filtro: %s\n", errbuf);
       return EXIT_FAILURE;
     }

     if(pcap_setfilter(captura, &fp) == -1) {
       printf("(ERROR) No se puede aplicar filtro.\n");
       return EXIT_FAILURE;
     }

     printf("Escuchando en el puerto 80.. \n");
     pcap_loop(captura, -1, callback, NULL);

     return EXIT_SUCCESS;
 }

/**
 * Selecciona una interfaz de red y la pasa como argumento para iniciar
 * captura de paquetes.
 * @return int estado de ejecución
 */
 int sel_device()
 {
   char ebuf[PCAP_ERRBUF_SIZE];
   pcap_if_t* deviceList;

   if(pcap_findalldevs(&deviceList,ebuf) == -1) {
     printf("No se pueden listar las interfaces.\nERROR: %s", ebuf);
     return EXIT_FAILURE;
   }

   char c;
   while(deviceList->next != NULL) {
       printf("%s [Y/n]: ", (deviceList->name));
       c = getchar(); getchar(); // reads newline

       if(c == 'Y' || c == 'y') {
         printf("\nInterfaz seleccionada.\n");
         return sniff(deviceList->name);
       }

       deviceList = deviceList->next;
   }

   printf("No se ha seleccionado interfaz.. abortando.");
   return EXIT_FAILURE;
 }

 int main () {
   sel_device();

   return 0;
}
