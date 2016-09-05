CC=gcc
CFLAGS=-lpcap
SOURCES=pcap.c
EXECUTABLE=captura

all:
	$(CC) $(SOURCES) -o $(EXECUTABLE) $(CFLAGS)
	sudo ./$(EXECUTABLE)

clean:
	rm $(EXECUTABLE)

run:
	sudo ./$(EXECUTABLE)
