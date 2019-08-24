#!/usr/bin/env python

import os, glob
from logging import info, debug

from Layouts import Layouts
from prompt_toolkit.buffer import Buffer

class ContentManager:

    def __init__(self, studio):
        self.studio = studio
        
        self.bufferSpecs = [
            #(buffer name, initial value, location, update function)

            ("statusBar", "TensorStudio", Layouts.HOME, None),
            ("savedModels",      None, Layouts.HOME, self.studio.controller.fileLister("saved_models", outputFormat=str)),
            ("modelDefinitions", None, Layouts.HOME, self.studio.controller.fileLister("model_definitions", outputFormat=str)),
        ]

        self.bufferStore = self.initializeBuffers()

    # ------------- Primary API ----------------#

    def getBuffer(self, buffName, giveAll=False):

        #giveAll -> returns buffer, location, and updateFunction
        if giveAll:
            return self.bufferStore[buffName]

        #otherwise just return the buffer
        buff, _, _ = self.bufferStore[buffName]
        return buff

    def setText(self, buffName, text):
        buff = self.getBuffer(buffName)
        buff.text = text

    def updateText(self, buffName):
        buff, _, updateFunction = self.getBuffer(buffName, giveAll=True)

        if not callable(updateFunction):
            return

        buff.text = updateFunction()

        return buff.text

    def updateLocation(self, location):
        #if passed Layouts.ALL -> update all buffers
        if location == Layouts.ALL:
            for buffName in self.bufferStore:
                self.updateText(buffName)
            return

        #otherwise update buffers at given location and buffers at Layouts.ALL
        for buffName, (_, buffLocation, _) in self.bufferStore.items():
            if buffLocation == location or buffLocation == Layouts.ALL:
                self.updateText(buffName)


    # ------------- Handler factories ----------------#
    def locationUpdater(self, location):
        def handler(event=None):
            self.updateLocation(location)
        return handler


    # ------------- Helpers ----------------#
    def initializeBuffers(self):

        bufferStore = dict()

        for name, initialValue, location, updateFunction in self.bufferSpecs:
            buff = Buffer(name=name)

            if initialValue is not None:
                buff.text = initialValue
            elif updateFunction is not None:
                buff.text = updateFunction()

            bufferStore[name] = (buff, location, updateFunction)

        return bufferStore