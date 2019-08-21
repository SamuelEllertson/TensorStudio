#!/usr/bin/env python

from prompt_toolkit.layout import Container, Dimension, to_container

class Sizeable(Container):
    def __init__(self, item, w_min=None, w_max=None, w_pre=None, w_weight=None, h_min=None, h_max=None, h_pre=None, h_weight=None):
        super().__init__()
        self.item = to_container(item)
        self.width  = Dimension(min=w_min, max=w_max, preferred=w_pre, weight=w_weight)
        self.height = Dimension(min=h_min, max=h_max, preferred=h_pre, weight=h_weight)

    def reset(self):
        self.item.reset()

    def preferred_width(self, max_available_width: int) -> Dimension:
        return self.width

    def preferred_height(self, width: int, max_available_height: int) -> Dimension:
        return self.height

    def write_to_screen(self, screen, mouse_handlers, write_position, parent_style, erase_bg, z_index):
        self.item.write_to_screen(screen, mouse_handlers, write_position, parent_style, erase_bg, z_index)

    def is_modal(self):
        return self.item.is_modal()

    def get_key_bindings(self):
        return self.item.get_key_bindings()

    def get_children(self):
        return [self.item]

    def __pt_container__(self):
        return self.item