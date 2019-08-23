#!/usr/bin/env python

import os, glob

from prompt_toolkit.buffer import Buffer

class ContentManager:

    def __init__(self, studio):
        self.studio = studio
        self.homeStatusBarBuffer = self.getHomeStatusBarBuffer()
        self.homeSavedModelsBuffer = self.getHomeSavedModelsBuffer()
        self.homeModelDefinitionsBuffer = self.getHomeModelDefinitionsBuffer()


    # ------------- Buffer getters and setters ----------------#

    #>>>Home Status Bar stuff
    def getHomeStatusBarBuffer(self):
        #singlton
        try:
            return self.homeStatusBarBuffer
        except:
            pass

        #failed --> this is initialization:
        buff = Buffer()
        buff.text = "TensorStudio"

        return buff

    def setHomeStatusBarText(self, text):
        self.homeStatusBarBuffer.text = text

    #>>>Home Saved Models stuff
    def getHomeSavedModelsBuffer(self):
        #singlton
        try:
            return self.homeSavedModelsBuffer
        except:
            pass

        #failed --> this is initialization:
        buff = Buffer()
        buff.text = self.studio.controller.getSavedModelsList(outputFormat="string")

        return buff

    def updateHomeSavedModelsText(self):
        self.getHomeSavedModelsBuffer().text = self.studio.controller.getSavedModelsList(outputFormat="string")

    #>>>Home Model Definitions stuff
    def getHomeModelDefinitionsBuffer(self):
        #singlton
        try:
            return self.homeModelDefinitionsBuffer
        except:
            pass

        #failed --> this is initialization:
        buff = Buffer()
        buff.text = self.studio.controller.getModelDefinitionsList(outputFormat="string")

        return buff

    def updateHomeModelDefinitionsText(self):
        self.getHomeModelDefinitionsBuffer().text = self.studio.controller.getModelDefinitionsList(outputFormat="string")


    # ------------- Layout updating ----------------#
    def updateHomeContent(self, event=None):
        self.updateHomeSavedModelsText()
        self.updateHomeModelDefinitionsText()    

    def updateAllContent():###update with new layouts
        self.updateHomeContent()