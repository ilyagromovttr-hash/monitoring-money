import tkinter as tk
from ui.modules.currency_tracker import CurrencyTrackerModule
from ui.modules.finance_tracker import FinanceTrackerModule
from ui.modules.habit_tracker import HabitTrackerModule  # Импортируем новый трекер привычек
from ui.modules.stubs import StubModule

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python SuperApp v1.2")
        self.geometry("1050x650")
        self.minsize(950, 600)
        
        self.sidebar = tk.Frame(self, bg="#212529", width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        self.container = tk.Frame(self, bg="#f0f2f5")
        self.container.pack(side="right", fill="both", expand=True)
        
        self.modules = {}
        self.active_module = None
        
        self.build_sidebar()
        self.init_modules()
        self.show_module("currency")

    def build_sidebar(self):
        logo = tk.Label(self.sidebar, text="⚡ SUPERAPP", bg="#212529", fg="#ffffff", font=("Arial", 14, "bold"), pady=20)
        logo.pack(fill="x")
        
        btn_style = {
            "bg": "#343a40", "fg": "white", "relief": "flat", 
            "activebackground": "#495057", "activeforeground": "white", 
            "anchor": "w", "padx": 15, "pady": 10, "font": ("Arial", 10)
        }
        
        tk.Button(self.sidebar, text="📊 Мониторинг Валют", command=lambda: self.show_module("currency"), **btn_style).pack(fill="x", pady=1)
        tk.Button(self.sidebar, text="💰 Управление Бюджетом", command=lambda: self.show_module("finance"), **btn_style).pack(fill="x", pady=1)
        tk.Button(self.sidebar, text="✅ Трекер Привычек", command=lambda: self.show_module("habit"), **btn_style).pack(fill="x", pady=1) # Заменили заглушку
        
        for i in range(4, 6):
            tk.Button(self.sidebar, text=f"🛠 Утилита {i} (Заглушка)", command=lambda: self.show_module(f"stub{i}"), **btn_style).pack(fill="x", pady=1)

    def init_modules(self):
        self.modules["currency"] = CurrencyTrackerModule(self.container, self)
        self.modules["finance"] = FinanceTrackerModule(self.container, self)
        self.modules["habit"] = HabitTrackerModule(self.container, self) # Активируем модуль
        
        for i in range(4, 6):
            stub = StubModule(self.container, self)
            stub.set_title(f"Утилита №{i}\n(Модуль находится на стадии разработки)")
            self.modules[f"stub{i}"] = stub

    def show_module(self, name):
        if self.active_module:
            self.active_module.pack_forget()
            
        self.active_module = self.modules[name]
        self.active_module.pack(fill="both", expand=True)