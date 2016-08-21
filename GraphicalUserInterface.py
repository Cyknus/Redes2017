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

######################################################
# ACTUALIZACIÓN                                      #
# La GUI será en Kivy 1.9.1                          #
# Así que será necesario instalar kivy 1.9.1         #
######################################################
import sys, getopt



# **************************************************
#  Definicion de la funcion principal
#**************************************************
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "l", ["local="])
    except getopt.GetoptError:
        #TODO lanzar exepcion
    if opts: #Si el usuario mandó alguna bandera
        local = True if '-l' in opts[0] else False
    else:
        local = False
    app = QtGui.QApplication(sys.argv)
    #TODO Llamar a su ventana de login
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv[1:])
