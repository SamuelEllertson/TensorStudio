#!/usr/bin/env python

import os, glob

from prompt_toolkit.filters import Condition

class TensorController:

    def __init__(self):
        self.workingModel = None
        self.trainingModel = None

    #------------- Filters ----------------#

    #These are function factories because Conditions cant have arguments, but we still need the instance 'self' reference.

    def getWorkingModelExistsHandler(self):
        @Condition
        def workingModelExists():
            if self.workingModel is not None:
                return True
            return False
        return workingModelExists


    # ------------- Model list stuff ----------------#
    def getSavedModelsList(self, outputFormat="list"):

        models = [os.path.basename(f) for f in glob.glob("./saved_models/*")]

        if outputFormat == "list":
            return models

        if outputFormat == "string":
            return "\n".join(models)

    def getModelDefinitionsList(self, outputFormat="list"):

        models = [os.path.basename(f) for f in glob.glob("./model_definitions/*")]

        if outputFormat == "list":
            return models

        if outputFormat == "string":
            return "\n".join(models)


    # ------------- Loading model stuff ----------------#
    def loadSavedModel(self, modelName):
        pass

    def loadModelFromDefinition(self, modelName):
        pass
