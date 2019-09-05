#!/usr/bin/env python
"""
Represents the fullscreen app
"""
import logging
from logging import info, debug

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

        #initialize only after all managers have been instantiated due to cyclic dependencies between them
        self.controller.initializeController()
        self.content.initializeContent()
        self.layouts.initializeLayouts()
        self.keyBindings.initializeKeyBinds()

        #the prompt_toolkit Application object
        self.app = self.initializeApp() 

    # ------------- Helpers ----------------#

    def initializeApp(self):
        layout = self.layouts.getLayout(self.location)
        style = self.layouts.getStyle()
        keyBindings = self.keyBindings.getGlobalKeyBinds()

        return Application(
            layout=layout,
            key_bindings=keyBindings,
            style=style,
            full_screen=True
        )

    def run(self):
        self.app.run()

    def exit(self, event=None):
        self.app.exit()


def main():
    TensorStudio().run()

if __name__ == '__main__':
    main()