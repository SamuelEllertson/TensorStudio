#!/usr/bin/env python

from logging import info, debug

from prompt_toolkit.key_binding import KeyBindings, DynamicKeyBindings
from prompt_toolkit.key_binding.bindings.focus import (focus_next, focus_previous)

from LayoutManager import Layouts

class KeyBindingsManager:

    def __init__(self, studio):
        self.studio = studio
        
        self.keyBindSpecs = [
            #(location, keybindFactory)

            #Layouts.ALL represents the global, dynamic keybinds used by the app here
            (Layouts.ALL, self.dynamicKeyBinds),

            #The keybinds per layout
            (Layouts.HOME, self.homeKeybinds),
            (Layouts.CREATE, self.creationKeybinds),
        ]

        #self.keyBindingsStore = self.initializeKeyBinds()

    # ------------- Primary API ----------------#

    def getGlobalKeyBinds(self):
        return self.get(Layouts.ALL)

    def get(self, location):
        return self.keyBindingsStore[location]

    # ------------- KeyBind Factories ----------------# 

    def dynamicKeyBinds(self):
        return DynamicKeyBindings(self.getRelevantKeyBindings)

    def homeKeybinds(self):
        kb = KeyBindings()

        #Exit on q and control + q
        kb.add("q", eager=True)(self.studio.exit)
        kb.add("c-q", eager=True)(self.studio.exit)

        #C to load creation layout
        kb.add("c")(self.studio.layouts.swapper(Layouts.CREATE))

        #E to edit model only if a model is loaded
        kb.add("e", filter=self.studio.controller.modelExistsFilter())(self.studio.layouts.swapper(Layouts.EDIT))

        #tab and down focus next button
        kb.add("tab")(focus_next)
        kb.add("down")(focus_next)

        #shift + tab and up focus previous button
        kb.add("s-tab")(focus_previous)
        kb.add("up")(focus_previous)

        ###REMOVE
        kb.add("r")(self.studio.content.locationUpdater(Layouts.HOME))
        kb.add("t")(self.test) ###REMOVE: TESTING PURPOSES ONLY

        return kb

    def creationKeybinds(self):
        kb = KeyBindings()

        #Exit on control + q
        kb.add("c-q", eager=True)(self.studio.exit)

        #Escape returns to home
        kb.add("escape")(self.studio.layouts.swapper(Layouts.HOME)) ###todo: saving logic

        return kb

    # ------------- Helpers ----------------#

    def test(self, event=None):###REMOVE LATER: TESTING PURPOSES ONLY
        if self.studio.controller.workingModel is None:
            self.studio.controller.workingModel = True
        else:
            self.studio.controller.workingModel = None 

    def getRelevantKeyBindings(self):
        return self.get(self.studio.location)

    def initializeKeyBinds(self):

        keyBindingsStore = dict()

        for location, factoryFunction in self.keyBindSpecs:
            keyBindingsStore[location] = factoryFunction()

        self.keyBindingsStore = keyBindingsStore