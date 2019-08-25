#!/usr/bin/env python

import os, glob

from prompt_toolkit.filters import Condition

class TensorController:

    def __init__(self, studio):
        self.studio = studio
        self.workingModel = None
        self.trainingModel = None

    # ------------- Handler Factories ----------------#

    def fileLister(self, directory, outputFormat=str):

        def lister():
            theList = self.getFilesList(directory)

            if outputFormat == str:
                return "\n".join(theList)

            if outputFormat == list:
                return theList

        return lister

    # ------------- Loading model stuff ----------------#

    def loadSavedModel(self, modelName):
        pass

    def loadModelFromDefinition(self, modelName):
        pass

    #------------- Filters ----------------#
    #These are function factories because Conditions can't have arguments, but we still need the instance 'self' reference.

    def modelExistsFilter(self):
        @Condition
        def workingModelExists():
            if self.workingModel is not None:
                return True
            return False
        return workingModelExists

    # ------------- Helper functions ----------------#

    def getFilesList(self, directory):
        files = [os.path.basename(f) for f in glob.glob(f"./{directory}/*")]
        return files

    def initializeController(self):
        pass