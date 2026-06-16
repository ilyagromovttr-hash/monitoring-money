import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ui.modules.base_module import BaseModule
from core.habit_service import HabitService
from datetime import datetime

class HabitTrackerModule(BaseModule):
    def build_ui(self):
        self.configure(bg="#f0f2f5")
        
        # Верхняя панель управления
        top_bar = tk.Frame(self, bg="#ffffff", bd=1, relief="solid", padx=10, pady=10)
        top_bar.pack(fill="x", padx=10, pady=10)
        
        tk.Label(top_bar, text="Новая привычка:", bg="#ffffff", font=("Arial", 10)).pack(side="left", padx=(0, 5))
        self.ent_habit_name = ttk.Entry(top_bar, width=30)
        self.ent_habit_name.pack(side="left", padx=(0, 10))
        
        btn_add = tk.Button(top_bar, text="➕ Создать", command=self.add_habit, bg="#28a745", fg="white", relief="flat", font=("Arial", 9, "bold"), padx=10)
        btn_add.pack(side="left", padx=5)
        
        btn_export = tk.Button(top_bar, text="📤 Экспорт", command=self.export_habits, bg="#17a2b8", fg="white", relief="flat", font=("Arial", 9))
        btn_export.pack(side="right", padx=5)
        
        btn_import = tk.Button(top_bar, text="📥 Импорт", command=self.import_habits, bg="#ffc107", fg="black", relief="flat", font=("Arial", 9))
        btn_import.pack(side="right", padx=5)

        # Главная таблица со списком привычек
        table_frame = tk.Frame(self, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        columns = ("id", "name", "status", "current_streak", "best_streak")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Привычка")
        self.tree.heading("status", text="Статус сегодня")
        self.tree.heading("current_streak", text="Текущая серия (дн.)")
        self.tree.heading("best_streak", text="Лучшая серия (дн.)")
        
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("name", width=250, anchor="w")
        self.tree.column("status", width=130, anchor="center")
        self.tree.column("current_streak", width=140, anchor="center")
        self.tree.column("best_streak", width=140, anchor="center")
        self.tree.pack(fill="both", expand=True, side="left")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Нижняя панель действий над выбранной привычкой
        action_bar = tk.Frame(self, bg="#f0f2f5")
        action_bar.pack(fill="x", padx=10, pady=(0, 10))
        
        btn_done = tk.Button(action_bar, text="✅ Выполнено", command=lambda: self.mark_habit("done"), bg="#28a745", fg="white", font=("Arial", 10, "bold"), relief="flat", width=15, pady=5)
        btn_done.pack(side="left", padx=(0, 10))
        
        btn_skip = tk.Button(action_bar, text="❌ Пропущено", command=lambda: self.mark_habit("skipped"), bg="#dc3545", fg="white", font=("Arial", 10, "bold"), relief="flat", width=15, pady=5)
        btn_skip.pack(side="left", padx=(0, 20))
        
        btn_edit = tk.Button(action_bar, text="✏️ Редактировать", command=self.edit_habit, bg="#6c757d", fg="white", font=("Arial", 9), relief="flat", pady=5)
        btn_edit.pack(side="left", padx=5)
        
        btn_del = tk.Button(action_bar, text="🗑 Удалить", command=self.delete_habit, bg="#343a40", fg="white", font=("Arial", 9), relief="flat", pady=5)
        btn_del.pack(side="left", padx=5)

        self.refresh_list()

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        data = HabitService.load_data()
        today_str = datetime.now().strftime("%d.%m.%Y")
        
        for h in data["habits"]:
            # Получаем статус на сегодня
            status_today = "⏳ Не отмечено"
            if today_str in h["history"]:
                status_today = "🟢 Выполнено" if h["history"][today_str] == "done" else "🔴 Пропущено"
                
            # Считаем серии
            curr_str, best_str = HabitService.calculate_streaks(h["history"])
            
            self.tree.insert("", "end", values=(h["id"], h["name"], status_today, curr_str, best_str))

    def add_habit(self):
        name = self.ent_habit_name.get().strip()
        if not name:
            messagebox.showwarning("Внимание", "Введите название привычки.")
            return
        HabitService.add_habit(name)
        self.ent_habit_name.delete(0, tk.END)
        self.refresh_list()

    def get_selected_habit_id(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите привычку из списка.")
            return None
        return self.tree.item(selected[0])["values"][0]

    def mark_habit(self, status):
        habit_id = self.get_selected_habit_id()
        if habit_id is None:
            return
        success, msg = HabitService.mark_habit(habit_id, status)
        if success:
            self.refresh_list()
        else:
            messagebox.showwarning("Ограничение", msg)

    def edit_habit(self):
        habit_id = self.get_selected_habit_id()
        if habit_id is None:
            return
            
        # Просим ввести новое имя через простое окно ввода
        from tkinter import simpledialog
        current_name = ""
        data = HabitService.load_data()
        for h in data["habits"]:
            if h["id"] == habit_id:
                current_name = h["name"]
                
        new_name = simpledialog.askstring("Редактирование", "Введите новое название привычки:", initialvalue=current_name)
        if new_name and new_name.strip():
            HabitService.edit_habit(habit_id, new_name.strip())
            self.refresh_list()

    def delete_habit(self):
        habit_id = self.get_selected_habit_id()
        if habit_id is None:
            return
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить привычку?"):
            HabitService.delete_habit(habit_id)
            self.refresh_list()

    def export_habits(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filepath:
            HabitService.export_data(filepath)
            messagebox.showinfo("Успех", "Данные успешно экспортированы!")

    def import_habits(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if filepath:
            if HabitService.import_data(filepath):
                self.refresh_list()
                messagebox.showinfo("Успех", "Данные успешно импортированы!")
            else:
                messagebox.showerror("Ошибка", "Не удалось прочитать файл резервной копии.")