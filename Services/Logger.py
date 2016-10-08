#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

class Logger(object):
    """Generates a custom logger for the project"""
    def __init__(self):
        super(Logger, self).__init__()

    @staticmethod
    def getFor(name):
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(name)-12s %(asctime)s :: %(message)s')
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger
