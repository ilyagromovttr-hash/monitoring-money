import tkinter as tk
from ui.modules.base_module import BaseModule

class StubModule(BaseModule):
    def set_title(self, title_text):
        self.configure(bg="#f0f2f5")
        label = tk.Label(
            self, 
            text=f"Тут будет находиться\n{title_text}", 
            font=("Arial", 16, "italic"), 
            bg="#f0f2f5", 
            fg="#6c757d"
        )
        label.pack(expand=True)