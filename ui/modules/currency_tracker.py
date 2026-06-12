import tkinter as tk
from tkinter import ttk, messagebox
from ui.modules.base_module import BaseModule
from core.cbr_service import CBRService
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class CurrencyTrackerModule(BaseModule):
    def build_ui(self):
        self.configure(bg="#f0f2f5")
        
        # Данные
        self.rates_data = CBRService.get_daily_rates()
        
        # Верхняя панель управления
        control_panel = tk.Frame(self, bg="#ffffff", height=60, bd=1, relief="solid")
        control_panel.pack(fill="x", side="top", padx=10, pady=10)
        
        tk.Label(control_panel, text="Валюта:", bg="#ffffff", font=("Arial", 10, "bold")).pack(side="left", padx=10)
        self.currency_combo = ttk.Combobox(control_panel, values=list(self.rates_data.keys()), state="readonly", width=10)
        self.currency_combo.pack(side="left", padx=5)
        if self.rates_data:
            self.currency_combo.current(0)
            
        tk.Label(control_panel, text="Период (дней назад):", bg="#ffffff", font=("Arial", 10, "bold")).pack(side="left", padx=10)
        self.period_spin = ttk.Spinbox(control_panel, from_=7, to=365, width=5)
        self.period_spin.set(30)
        self.period_spin.pack(side="left", padx=5)
        
        btn_update = tk.Button(control_panel, text="Построить график", command=self.update_chart, bg="#007bff", fg="white", font=("Arial", 9, "bold"), relief="flat", padx=10)
        btn_update.pack(side="left", padx=15)

        # Контейнер для графика
        self.chart_frame = tk.Frame(self, bg="#ffffff", bd=1, relief="solid")
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Инициализация пустого графика
        self.fig, self.ax = plt.subplots(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Панель инструментов Matplotlib (зум, сохранение)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.chart_frame)
        self.toolbar.update()
        
        self.update_chart()

    def update_chart(self):
        char_code = self.currency_combo.get()
        if not char_code or not self.rates_data:
            messagebox.showerror("Ошибка", "Данные ЦБ недоступны.")
            return
            
        valute_id = self.rates_data[char_code]['id']
        days = int(self.period_spin.get())
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        dates, values = CBRService.get_history(
            valute_id, 
            start_date.strftime("%d/%m/%Y"), 
            end_date.strftime("%d/%m/%Y")
        )
        
        self.ax.clear()
        if dates and values:
            self.ax.plot(dates, values, marker='o', color='#007bff', linewidth=2, markersize=4, label=f"1 {char_code} в RUB")
            self.ax.set_title(f"Динамика курса: {self.rates_data[char_code]['name']}", fontsize=11, fontweight='bold')
            self.ax.grid(True, linestyle='--', alpha=0.6)
            self.ax.legend()
            self.fig.autofmt_xdate()
        else:
            self.ax.text(0.5, 0.5, "Нет данных за выбранный период", ha='center', va='center')
            
        self.canvas.draw()