#! /usr/bin/env python3
# -*- coding: utf-8 -*-

######################################################
# PURPOSE:Interfaz grafica de un cliente en PyQt4    #
#                                                    #
# Vilchis Dominguez Miguel Alonso                    #
#       <mvilchis@ciencias.unam.mx>                  #
#                                                    #
# Notes: El alumno tiene que implementar la parte    #
#       comentada como TODO(Instalar python-qt)      #
#                                                    #
# Copyright   16-08-2015                             #
#                                                    #
# Distributed under terms of the MIT license.        #
#################################################### #

##########################################################
# ACTUALIZACIÓN                                          #
# La GUI será en Kivy 1.9.1                              #
# GUI: https://kivy.org/#home                            #
# Así que será necesario instalar kivy 1.9.1             #
# Ejecución: python3 GraphicalUserInterface.py -- [args] #                                                    #
##########################################################
import sys, getopt
from GUI.Chat import build_screen_manager

# **************************************************
#  Definicion de la funcion principal
#**************************************************
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "l", ["local="])
    except getopt.GetoptError:
        print("whaaat?")

    if opts: #Si el usuario mandó alguna bandera
        local = True if "-l" in opts[0] else False
    else:
        local = False

    app = build_screen_manager(local)
    app.run()

if __name__ == '__main__':
    main(sys.argv[1:])
