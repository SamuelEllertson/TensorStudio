#!/usr/bin/env python

from logging import info, debug
from enum import Enum

from prompt_toolkit.key_binding.bindings.focus import (focus_next, focus_previous)
from prompt_toolkit.layout import HSplit, Layout, VSplit, Window, BufferControl, WindowAlign, ConditionalContainer
from prompt_toolkit.layout import Dimension as D
from prompt_toolkit.widgets import Box, Button, Frame, Label, TextArea, HorizontalLine
from prompt_toolkit.styles import Style

from Sizeable import Sizeable


class Layouts(Enum):
    ALL = 0
    HOME = 1
    CREATE = 2
    LOAD = 3
    IMPORT = 4
    EDIT = 5

class LayoutManager:

    def __init__(self, studio):
        self.studio = studio
        
        self.layoutSpecs = [
            #(layoutName, location, layoutFactoryFunc)

            ("home", Layouts.HOME, self.homeLayoutFactory),
            ("create", Layouts.CREATE, self.creationLayoutFactory),
        ]

        self.layoutStore = self.initializeLayouts()

    # ------------- Primary API ----------------#

    def getLayout(self, layoutNameOrLocation):
        return self.layoutStore[layoutNameOrLocation]

    def resolveLocation(self, layoutNameOrLocation):
        #case: Already is a location -> return it
        if isinstance(layoutNameOrLocation, Layouts):
            return layoutNameOrLocation

        #case: is a string -> try to resolve it
        elif isinstance(layoutNameOrLocation, str):

            #iterate over the layout specs for the name
            for name, location, _ in self.layoutSpecs:
                if name == layoutName:
                    return location

            #raise KeyError if the name doesnt exist
            raise KeyError(f"layoutName '{layoutName}' does not exist")

        #case: not an int or string -> TypeError
        raise TypeError(f"received {type(layoutNameOrLocation)} was expecting int or string")

    def getStyle(self):

        return Style.from_dict({
            'homeleftsidebar':  'bg:#888800 #000000',
            'homerightsidebar': 'bg:#00aa00 #000000',
            'statusbar': 'bg:#ffffff fg:#000000 bold',
            'blackonwhite': 'bg:#ffffff fg:#000000',
            'blue':'fg:#0000ff',
            'button':'',
            'button.focused':'noinherit blue bold',
            'underlined':'underline',
            'frame':'white',
            'cursor':'blue',
        })

    # ------------- Layout Factories ----------------#

    def homeLayoutFactory(self):
        content = self.studio.content

        statusBar = \
        Frame(
            Window(
                BufferControl(buffer=content.getBuffer("statusBar"), focusable=False), 
                height=D(min=1, max=1, preferred=1),
                align=WindowAlign.CENTER
            )
        )

        savedModelsBox = \
        Box(
            HSplit([
                Label(text="Saved Models: ", style="class:blue class:underlined"),
                Window(
                    BufferControl(buffer=content.getBuffer("savedModels"), focusable=False)
                )
            ]),
            padding=0
        )

        modelDefinitionsBox = \
        Box(
            HSplit([
                Label(text="Model Definitions: ", style="class:blue class:underlined"),
                Window(
                    BufferControl(buffer=content.getBuffer("modelDefinitions"), focusable=False)
                )
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

        createModelButton = Button("[C] Create Model                 ", handler=self.studio.swapHandlerFactory(Layouts.CREATE))
        loadModelButton   = Button("[L] Load Saved Model             ", handler=self.studio.swapHandlerFactory(Layouts.LOAD))
        importModelButton = Button("[I] Import Model From Definition ", handler=self.studio.swapHandlerFactory(Layouts.IMPORT))
        editModelButton   = Button("[E] Edit Model                   ", handler=self.studio.swapHandlerFactory(Layouts.EDIT))
        quitButton        = Button("[Q] Quit                         ", handler=self.studio.exit)

        editModelButton = ConditionalContainer(editModelButton, filter=self.studio.controller.modelExistsHandler())

        buttons = \
        HSplit([
            createModelButton,
            loadModelButton,
            importModelButton,
            editModelButton,
            quitButton,
        ])

        creditBar = Label(text="Created by Samuel Ellertson - github.com/SamuelEllertson", style="class:blue")

        leftSidebar = buttons

        body = \
        VSplit([
            Frame(Sizeable(leftSidebar)),
            Sizeable(rightSidebar)
        ])

        root = \
        HSplit([
            statusBar,
            body,
            creditBar
        ])

        return Layout(
            container=root,
            focused_element=createModelButton
        )


    def creationLayoutFactory(self):
        content = self.studio.content

        root_container = Box(
            Frame(TextArea(
                text="Creation layout placeholder",
                width=40,
                height=10,
            )),
        )

        return Layout(container=root_container)


    # ------------- Helpers ----------------#
    def initializeLayouts(self):
        layoutStore = dict()

        for layoutName, location, creationFunction in self.layoutSpecs:
            layout = creationFunction()

            #two entries so that layout can be retrieved by its name or location
            layoutStore[layoutName] = layout
            layoutStore[location] = layout

        return layoutStore