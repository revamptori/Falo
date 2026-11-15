from dataclasses import dataclass, field
from typing import List

class Widget:
    pass

@dataclass
class Button(Widget):
    label: str
    on_click: callable = None
    def click(self):
        if self.on_click: self.on_click()

@dataclass
class Label(Widget):
    text: str

class UICanvas:
    def __init__(self):
        self.widgets: List[Widget] = []
        self.theme = "dark"

    def add(self, w: Widget): self.widgets.append(w)
    def button(self, label, on_click=None): b=Button(label, on_click); self.add(b); return b
    def label(self, text): l=Label(text); self.add(l); return l
