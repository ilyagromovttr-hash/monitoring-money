import tkinter as tk
from tkinter import ttk, messagebox
from ui.modules.base_module import BaseModule
from core.finance_service import FinanceService
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FinanceTrackerModule(BaseModule):
    def build_ui(self):
        self.configure(bg="#f0f2f5")
        
        # Главный контейнер (делим экран на левую и правую колонки)
        main_box = tk.Frame(self, bg="#f0f2f5")
        main_box.pack(fill="both", expand=True, padx=10, pady=10)
        
        left_panel = tk.Frame(main_box, bg="#f0f2f5", width=380)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_panel = tk.Frame(main_box, bg="#f0f2f5")
        right_panel.pack(side="right", fill="both", expand=True)

        # ---------------- ЛЕВАЯ ПАНЕЛЬ: УПРАВЛЕНИЕ ----------------
        # 1. Блок баланса
        bal_frame = tk.Frame(left_panel, bg="#ffffff", bd=1, relief="solid", padx=15, pady=10)
        bal_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(bal_frame, text="Текущий баланс:", bg="#ffffff", font=("Arial", 11)).pack(anchor="w")
        self.lbl_balance = tk.Label(bal_frame, text="0.00 руб.", bg="#ffffff", fg="#28a745", font=("Arial", 18, "bold"))
        self.lbl_balance.pack(anchor="w")

        # 2. Блок добавления транзакции
        tx_frame = tk.LabelFrame(left_panel, text=" Добавить операцию ", bg="#ffffff", font=("Arial", 10, "bold"), padx=10, pady=10)
        tx_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(tx_frame, text="Тип:", bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_type = ttk.Combobox(tx_frame, values=["Доход", "Расход"], state="readonly", width=12)
        self.combo_type.grid(row=0, column=1, sticky="w", padx=5)
        self.combo_type.current(1)
        
        tk.Label(tx_frame, text="Категория:", bg="#ffffff").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_cat = ttk.Combobox(tx_frame, state="readonly", width=18)
        self.combo_cat.grid(row=1, column=1, sticky="w", padx=5)
        
        tk.Label(tx_frame, text="Сумма:", bg="#ffffff").grid(row=2, column=0, sticky="w", pady=5)
        self.ent_amount = ttk.Entry(tx_frame, width=12)
        self.ent_amount.grid(row=2, column=1, sticky="w", padx=5)
        
        btn_add_tx = tk.Button(tx_frame, text="Добавить", command=self.save_tx, bg="#28a745", fg="white", font=("Arial", 9, "bold"), relief="flat", padx=10)
        btn_add_tx.grid(row=2, column=2, padx=5)

        # 3. Блок добавления новой категории
        cat_frame = tk.LabelFrame(left_panel, text=" Создать свою категорию ", bg="#ffffff", font=("Arial", 10, "bold"), padx=10, pady=10)
        cat_frame.pack(fill="x", pady=(0, 10))
        
        self.ent_new_cat = ttk.Entry(cat_frame, width=20)
        self.ent_new_cat.pack(side="left", padx=(0, 10))
        tk.Button(cat_frame, text="+ Категория", command=self.create_cat, bg="#17a2b8", fg="white", relief="flat", font=("Arial", 9, "bold")).pack(side="left")

        # 4. Блок Целей накоплений
        goal_frame = tk.LabelFrame(left_panel, text=" Цели накоплений ", bg="#ffffff", font=("Arial", 10, "bold"), padx=10, pady=10)
        goal_frame.pack(fill="both", expand=True)
        
        goal_input = tk.Frame(goal_frame, bg="#ffffff")
        goal_input.pack(fill="x", pady=(0, 5))
        
        self.ent_goal_name = ttk.Entry(goal_input, width=15)
        self.ent_goal_name.insert(0, "Название цели")
        self.ent_goal_name.pack(side="left", padx=2)
        
        self.ent_goal_target = ttk.Entry(goal_input, width=8)
        self.ent_goal_target.insert(0, "Сумма")
        self.ent_goal_target.pack(side="left", padx=2)
        
        tk.Button(goal_input, text="Добавить цель", command=self.create_goal, bg="#6f42c1", fg="white", font=("Arial", 8, "bold"), relief="flat").pack(side="left", padx=5)

        self.goal_listbox = tk.Listbox(goal_frame, height=4, font=("Arial", 9))
        self.goal_listbox.pack(fill="both", expand=True, pady=5)
        
        goal_actions = tk.Frame(goal_frame, bg="#ffffff")
        goal_actions.pack(fill="x")
        self.ent_goal_deposit = ttk.Entry(goal_actions, width=10)
        self.ent_goal_deposit.pack(side="left", padx=(0, 5))
        tk.Button(goal_actions, text="Пополнить выбранную цель", command=self.deposit_goal, bg="#fd7e14", fg="white", font=("Arial", 8, "bold"), relief="flat").pack(side="left")

        # ---------------- ПРАВАЯ ПАНЕЛЬ: ИСТОРИЯ И ГРАФИК ----------------
        # Последние 10 транзакций
        hist_frame = tk.LabelFrame(right_panel, text=" Последние 10 транзакций ", bg="#ffffff", font=("Arial", 10, "bold"), padx=10, pady=10)
        hist_frame.pack(fill="x", pady=(0, 10))
        
        self.tx_tree = ttk.Treeview(hist_frame, columns=("date", "type", "cat", "amount"), show="headings", height=5)
        self.tx_tree.heading("date", text="Дата")
        self.tx_tree.heading("type", text="Тип")
        self.tx_tree.heading("cat", text="Категория")
        self.tx_tree.heading("amount", text="Сумма")
        self.tx_tree.column("date", width=110)
        self.tx_tree.column("type", width=60)
        self.tx_tree.column("cat", width=100)
        self.tx_tree.column("amount", width=80)
        self.tx_tree.pack(fill="x")

        # Область Круговой диаграммы
        chart_box = tk.LabelFrame(right_panel, text=" Распределение расходов за месяц ", bg="#ffffff", font=("Arial", 10, "bold"))
        chart_box.pack(fill="both", expand=True)
        
        self.fig, self.ax = plt.subplots(figsize=(4, 3), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_box)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        self.refresh_data()

    def refresh_data(self):
        summary = FinanceService.get_summary()
        
        # Обновляем баланс
        self.lbl_balance.config(text=f"{summary['balance']:.2f} руб.")
        if summary['balance'] < 0:
            self.lbl_balance.config(fg="#dc3545")
        else:
            self.lbl_balance.config(fg="#28a745")
            
        # Обновляем выпадающий список категорий
        self.combo_cat["values"] = summary["categories"]
        if summary["categories"]:
            self.combo_cat.current(0)
            
        # Обновляем таблицу транзакций
        for item in self.tx_tree.get_children():
            self.tx_tree.delete(item)
        for t in summary["last_10"]:
            color = "#28a745" if t["type"] == "Доход" else "#dc3545"
            self.tx_tree.insert("", "end", values=(t["date"], t["type"], t["category"], f"{t['amount']:.2f}"))

        # Обновляем цели
        self.goal_listbox.delete(0, tk.END)
        for g in summary["goals"]:
            progress = (g["current"] / g["target"] * 100) if g["target"] > 0 else 0
            self.goal_listbox.insert(tk.END, f"{g['name']}: {g['current']:.1f}/{g['target']:.1f} руб. ({progress:.1f}%)")

        # Рисуем круговую диаграмму расходов
        self.ax.clear()
        chart_data = summary["expense_chart_data"]
        if chart_data:
            labels = list(chart_data.keys())
            sizes = list(chart_data.values())
            self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
            self.ax.axis('equal')
        else:
            self.ax.text(0.5, 0.5, "Расходов пока нет", ha='center', va='center', fontsize=12)
        self.canvas.draw()

    def save_tx(self):
        t_type = self.combo_type.get()
        category = self.combo_cat.get()
        amount = self.ent_amount.get()
        
        if not amount:
            messagebox.showwarning("Внимание", "Введите сумму.")
            return
        try:
            FinanceService.add_transaction(t_type, category, amount)
            self.ent_amount.delete(0, tk.END)
            self.refresh_data()
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма должна быть числом.")

    def create_cat(self):
        new_cat = self.ent_new_cat.get().strip()
        if not new_cat:
            return
        if FinanceService.add_category(new_cat):
            self.ent_new_cat.delete(0, tk.END)
            self.refresh_data()
        else:
            messagebox.showwarning("Внимание", "Такая категория уже есть.")

    def create_goal(self):
        name = self.ent_goal_name.get().strip()
        target = self.ent_goal_target.get().strip()
        if not name or name == "Название цели" or not target or target == "Сумма":
            return
        try:
            FinanceService.add_goal(name, target)
            self.ent_goal_name.delete(0, tk.END)
            self.ent_goal_target.delete(0, tk.END)
            self.refresh_data()
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма цели должна быть числом.")

    def deposit_goal(self):
        selected = self.goal_listbox.curselection()
        amount = self.ent_goal_deposit.get()
        if not selected or not amount:
            messagebox.showwarning("Внимание", "Выберите цель и введите сумму пополнения.")
            return
        try:
            FinanceService.update_goal_progress(selected[0], amount)
            self.ent_goal_deposit.delete(0, tk.END)
            self.refresh_data()
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма пополнения должна быть числом.")