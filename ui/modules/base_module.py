import tkinter as tk

class BaseModule(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        """Метод должен быть переопределен в дочерних классах"""
        pass