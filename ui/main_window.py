import tkinter as tk
from ui.modules.currency_tracker import CurrencyTrackerModule
from ui.modules.stubs import StubModule

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python SuperApp v1.0")
        self.geometry("900x600")
        self.minimum_size = (800, 500)
        
        # Макет: Боковое меню + Контентная область
        self.sidebar = tk.Frame(self, bg="#212529", width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        self.container = tk.Frame(self, bg="#f0f2f5")
        self.container.pack(side="right", fill="both", expand=True)
        
        # Хранилище активных модулей
        self.modules = {}
        self.active_module = None
        
        self.build_sidebar()
        self.init_modules()
        
        # По умолчанию открываем первую утилиту
        self.show_module("currency")

    def build_sidebar(self):
        # Логотип / Название приложения
        logo = tk.Label(self.sidebar, text="⚡ SUPERAPP", bg="#212529", fg="#ffffff", font=("Arial", 14, "bold"), pady=20)
        logo.pack(fill="x")
        
        # Настройки стилей кнопок меню
        btn_style = {"bg": "#343a40", "fg": "white", "relief": "flat", "activebackground": "#495057", "activeforeground": "white", "anchor": "w", "padx": 15, "pady": 10, "font": ("Arial", 10)}
        
        # Кнопки переключения
        tk.Button(self.sidebar, text="📊 Мониторинг Валют", command=lambda: self.show_module("currency"), **btn_style).pack(fill="x", pady=1)
        tk.Button(self.sidebar, text="🛠 Утилита 2 (Заглушка)", command=lambda: self.show_module("stub2"), **btn_style).pack(fill="x", pady=1)
        tk.Button(self.sidebar, text="🛠 Утилита 3 (Заглушка)", command=lambda: self.show_module("stub3"), **btn_style).pack(fill="x", pady=1)
        tk.Button(self.sidebar, text="🛠 Утилита 4 (Заглушка)", command=lambda: self.show_module("stub4"), **btn_style).pack(fill="x", pady=1)
        tk.Button(self.sidebar, text="🛠 Утилита 5 (Заглушка)", command=lambda: self.show_module("stub5"), **btn_style).pack(fill="x", pady=1)

    def init_modules(self):
        # Инициализируем полноценный модуль курса валют
        self.modules["currency"] = CurrencyTrackerModule(self.container, self)
        
        # Инициализируем заглушки под будущие модули недели
        for i in range(2, 6):
            stub = StubModule(self.container, self)
            stub.set_title(f"Утилита №{i}\n(Модуль находится на стадии разработки)")
            self.modules[f"stub{i}"] = stub

    def show_module(self, name):
        """Скрывает текущий модуль и отображает выбранный."""
        if self.active_module:
            self.active_module.pack_forget()
            
        self.active_module = self.modules[name]
        self.active_module.pack(fill="both", expand=True)