#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')

from GUI.screens import ChatApp

def main(local):
    chat = ChatApp(local)
    chat.run()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Run chat app")
    parser.add_argument('-l', '--local', required=False, help='Runs in local mode', default=False, nargs='?', const=True)
    args = parser.parse_args()
    main(args.local)
