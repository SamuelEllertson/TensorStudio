#!/usr/bin/env python
"""
Represents the fullscreen app
"""
import logging
from logging import info, debug
from glob import glob 

from prompt_toolkit.application import Application

from TensorController import TensorController
from ContentManager import ContentManager
from LayoutManager import LayoutManager, Layouts
from KeyBindingsManager import KeyBindingsManager

logging.basicConfig(filename="debug.log", level=logging.DEBUG)

class TensorStudio:

    def __init__(self):
        #default location is Home
        self.location = Layouts.HOME

        self.controller = TensorController(self)
        self.content = ContentManager(self)
        self.layouts = LayoutManager(self)
        self.keyBindings = KeyBindingsManager(self)

        #the prompt_toolkit Application object
        self.app = self.initializeApp()

    # ------------- Handler Factorys ----------------#    
    def swapHandlerFactory(self, layoutType):
        def handler(event=None):
            self.swapLayout(layoutType)
        return handler

    # ------------- Helpers ----------------#

    def initializeApp(self):
        layout = self.layouts.getLayout("home")
        style = self.layouts.getStyle()
        keyBindings = self.keyBindings.getGlobalKeyBinds()

        return Application(
            layout=layout,
            key_bindings=keyBindings,
            style=style,
            full_screen=True
        )

    def swapLayout(self, layoutNameOrLocation):
        location = self.layouts.resolveLocation(layoutNameOrLocation)

        #set the current location and change to the new layout
        self.location = location
        self.app.layout = self.layouts.getLayout(location)

        #Then update the content on the new layout
        self.content.updateLocation(location)

    def run(self):
        self.app.run()

    def exit(self, event=None):
        self.app.exit()


def main():
    TensorStudio().run()

if __name__ == '__main__':
    main()