#!/usr/bin/env python
"""
Represents the fullscreen app
"""
from enum import Enum

import logging
from logging import info, debug
logging.basicConfig(filename="debug.log", level=logging.INFO)

from prompt_toolkit.application import Application

from prompt_toolkit.key_binding import KeyBindings, DynamicKeyBindings
from prompt_toolkit.key_binding.bindings.focus import (focus_next, focus_previous)

from prompt_toolkit.layout import HSplit, Layout, VSplit, Window, BufferControl, WindowAlign
from prompt_toolkit.layout import Dimension as D
from prompt_toolkit.widgets import Box, Button, Frame, Label, TextArea, HorizontalLine
from prompt_toolkit.styles import Style

from prompt_toolkit.filters import Condition

from prompt_toolkit.formatted_text import HTML

from prompt_toolkit.buffer import Buffer

class Layouts(Enum):
    HOME = 1
    CREATE = 2
    LOAD = 3
    IMPORT = 4

class TensorStudio:

    def __init__(self):
        #default location is Home
        self.location = Layouts.HOME

        #Layouts and layout specific keybindings
        self.homeLayout = self.getHomeLayout()
        self.homeKeyBindings = self.getHomeKeyBindings()

        self.creationLayout = self.getCreationLayout()
        self.creationKeyBindings = self.getCreationKeyBindings()
        
        #app wide keybindings and style
        self.dynamicKeyBindings = self.getDynamicKeyBindings()
        self.style = self.getStyle()

        #the Application object
        self.app = self.getApp()

    # ------------- Handler Factory ----------------#    
    def swapHandlerFactory(self, layoutType):
        def handler(event=None):
            self.swapLayout(layoutType)
        return handler

    # ------------- Home Layout Stuff ----------------#
    def getHomeLayout(self): ###TODO
        #singleton
        try:
            return self.homeLayout
        except:
            pass

        #statusBar = Label(text=HTML("<style fg='black' bg='white'>Statusbar</style>"), style="class:statusbar")
        buff = Buffer()
        buff.text = "TensorStudio"
        statusBar = \
        Frame(
            Window(
                BufferControl(buffer=buff, focusable=False), 
                height=D(min=1, max=1, preferred=1),
                align=WindowAlign.CENTER
            )
        )

        savedModelsBox = \
        Box(
            HSplit([
                Label(text="Saved Models: ", style="class:blackonwhite"),
                TextArea(text="fake.model", focusable=False, read_only=True)
            ]),
            padding=0
        )

        modelDefinitionsBox = \
        Box(
            HSplit([
                Label(text="Model Definitions: ", style="class:blackonwhite"),
                TextArea(text="fake.definition", focusable=False, read_only=True)
            ]),
            padding=0
        )

        rightSidebar = \
        Frame(
            HSplit([
                savedModelsBox,
                HorizontalLine(),
                modelDefinitionsBox
            ])
        )

        createModelButton = Button("[C] Create Model                 ", handler=self.swapHandlerFactory(Layouts.CREATE))
        loadModelButton   = Button("[L] Load Saved Model             ", handler=self.swapHandlerFactory(Layouts.LOAD))
        importModelButton = Button("[I] Import Model From Definition ", handler=self.swapHandlerFactory(Layouts.IMPORT))
        quitButton        = Button("[Q] Quit                         ", handler=self.exit)

        buttons = \
        HSplit([
            createModelButton,
            loadModelButton,
            importModelButton,
            quitButton
        ])

        creditBar = Label(text="Created by Samuel Ellertson             ")

        leftSidebar = \
        Frame(
            HSplit([
                buttons,
                creditBar
            ])
        )   

        body = \
        VSplit([
            leftSidebar,
            rightSidebar
        ])

        root = \
        HSplit([
            statusBar,
            body
        ])

        self.homeLayout = Layout(
            container=root,
            focused_element=createModelButton
        )

        return self.homeLayout

    def getHomeKeyBindings(self): ###TODO
        #singleton
        try:
            return self.homeKeyBindings
        except:
            pass

        kb = KeyBindings()

        #Exit on q and control + q
        kb.add("q", eager=True)(self.exit)
        kb.add("c-q", eager=True)(self.exit)

        #tab and down focus next button
        kb.add("tab")(focus_next)
        kb.add("down")(focus_next)

        #shift + tab and up focus previous button
        kb.add("s-tab")(focus_previous)
        kb.add("up")(focus_previous)

        self.homeKeyBindings = kb
        return self.homeKeyBindings

    # ------------- Creation Layout Stuff ----------------#
    def getCreationLayout(self):###TODO: remove placeholder
        #singleton
        try:
            return self.creationLayout
        except:
            pass

        root_container = Box(
            Frame(TextArea(
                text='Hello world!\nPress control-c to quit.',
                width=40,
                height=10,
            )),
        )
        self.creationLayout = Layout(container=root_container)

        return self.creationLayout

    def getCreationKeyBindings(self):
        #singleton
        try:
            return self.creationKeyBindings
        except:
            pass

        kb = KeyBindings()

        #Exit on control + q
        kb.add("c-q", eager=True)(self.exit)

        #Escape returns to home
        kb.add("escape")(self.swapHandlerFactory(Layouts.HOME)) ###todo: saving logic

        self.creationKeyBindings = kb
        return self.creationKeyBindings

    # ------------- Key Bindings ----------------#
    def getRelevantKeyBindings(self): ###Update with new layouts
        if self.location == Layouts.HOME:
            return self.getHomeKeyBindings()

        if self.location == Layouts.CREATE:
            return self.getCreationKeyBindings()

    def getDynamicKeyBindings(self):
        #singleton
        try:
            return self.dynamicKeyBindings
        except:
            pass

        self.dynamicKeyBindings = DynamicKeyBindings(self.getRelevantKeyBindings)

        return self.dynamicKeyBindings

    # ------------- Style Stuff ----------------#
    def getStyle(self): ###TODO
        #singleton
        try:
            return self.style
        except:
            pass

        self.style = Style.from_dict({
            'homeleftsidebar':  'bg:#888800 #000000',
            'homerightsidebar': 'bg:#00aa00 #000000',
            'statusbar': 'bg:#ffffff fg:#000000 bold',
            'blackonwhite': 'bg:#ffffff fg:#000000'
        })

        return self.style

    # ------------- App Stuff ----------------#
    def getApp(self):
        #singleton
        try:
            return self.app
        except:
            pass

        #Otherwise first call: Create app with home layout
        layout = self.getHomeLayout()
        keyBindings = self.getDynamicKeyBindings()
        style = self.getStyle()

        self.app = Application(
            layout=layout,
            key_bindings=keyBindings,
            style=style,
            full_screen=True
        )

        return self.app

    def setLayout(self, layoutObject):
        self.getApp().layout = layoutObject

    def swapLayout(self, layoutType):###Update with new layouts

        info(f"swapLayout called with {layoutType}")

        self.location = layoutType

        if layoutType == Layouts.HOME:
            self.setLayout(self.getHomeLayout())

        if layoutType == Layouts.CREATE:
            self.setLayout(self.getCreationLayout())

    def run(self):
        self.getApp().run()

    def exit(self, event=None):
        self.getApp().exit()



def main():
    TensorStudio().run()

if __name__ == '__main__':
    main()