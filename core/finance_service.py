import json
import os
from datetime import datetime

DB_FILE = "finance_data.json"

class FinanceService:
    @staticmethod
    def load_data():
        if not os.path.exists(DB_FILE):
            return {
                "transactions": [],
                "categories": ["Стипендия", "Подработка", "Продукты", "Транспорт", "Развлечения", "Кафе"],
                "goals": []
            }
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"transactions": [], "categories": [], "goals": []}

    @staticmethod
    def save_data(data):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def add_transaction(t_type, category, amount):
        data = FinanceService.load_data()
        new_tx = {
            "type": t_type,  # "Доход" или "Расход"
            "category": category,
            "amount": float(amount),
            "date": datetime.now().strftime("%d.%m.%Y %H:%M")
        }
        data["transactions"].append(new_tx)
        FinanceService.save_data(data)

    @staticmethod
    def add_category(category):
        data = FinanceService.load_data()
        if category and category not in data["categories"]:
            data["categories"].append(category)
            FinanceService.save_data(data)
            return True
        return False

    @staticmethod
    def add_goal(name, target):
        data = FinanceService.load_data()
        data["goals"].append({"name": name, "target": float(target), "current": 0.0})
        FinanceService.save_data(data)

    @staticmethod
    def update_goal_progress(index, amount):
        data = FinanceService.load_data()
        if 0 <= index < len(data["goals"]):
            data["goals"][index]["current"] += float(amount)
            FinanceService.save_data(data)

    @staticmethod
    def get_summary():
        data = FinanceService.load_data()
        txs = data["transactions"]
        
        total_income = sum(t["amount"] for t in txs if t["type"] == "Доход")
        total_expense = sum(t["amount"] for t in txs if t["type"] == "Расход")
        balance = total_income - total_expense
        
        # Считаем расходы по категориям для круговой диаграммы
        expense_by_cat = {}
        for t in txs:
            if t["type"] == "Расход":
                expense_by_cat[t["category"]] = expense_by_cat.get(t["category"], 0) + t["amount"]
                
        return {
            "balance": balance,
            "last_10": txs[-10:][::-1], # последние 10 в обратном порядке
            "categories": data["categories"],
            "expense_chart_data": expense_by_cat,
            "goals": data["goals"]
        }