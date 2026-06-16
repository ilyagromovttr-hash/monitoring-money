import json
import os
from datetime import datetime, timedelta

HABITS_FILE = "habits_data.json"

class HabitService:
    @staticmethod
    def load_data():
        if not os.path.exists(HABITS_FILE):
            return {"habits": []}
        try:
            with open(HABITS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"habits": []}

    @staticmethod
    def save_data(data):
        with open(HABITS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def add_habit(name):
        data = HabitService.load_data()
        # Простая генерация ID
        new_id = max([h["id"] for h in data["habits"]], default=0) + 1
        new_habit = {
            "id": new_id,
            "name": name,
            "history": {}  # формат: {"15.06.2026": "done", "16.06.2026": "skipped"}
        }
        data["habits"].append(new_habit)
        HabitService.save_data(data)
        return new_habit

    @staticmethod
    def edit_habit(habit_id, new_name):
        data = HabitService.load_data()
        for h in data["habits"]:
            if h["id"] == habit_id:
                h["name"] = new_name
                HabitService.save_data(data)
                return True
        return False

    @staticmethod
    def delete_habit(habit_id):
        data = HabitService.load_data()
        data["habits"] = [h for h in data["habits"] if h["id"] != habit_id]
        HabitService.save_data(data)

    @staticmethod
    def mark_habit(habit_id, status):
        """status может быть 'done' или 'skipped'"""
        data = HabitService.load_data()
        today_str = datetime.now().strftime("%d.%m.%Y")
        
        for h in data["habits"]:
            if h["id"] == habit_id:
                if today_str in h["history"]:
                    return False, "Сегодня отметка уже поставлена!"
                h["history"][today_str] = status
                HabitService.save_data(data)
                return True, "Успешно отмечено!"
        return False, "Привычка не найдена."

    @staticmethod
    def calculate_streaks(history):
        """Возвращает (текущая_серия, лучшая_серия) на основе истории выполненных дней"""
        done_dates = []
        for date_str, status in history.items():
            if status == "done":
                try:
                    done_dates.append(datetime.strptime(date_str, "%d.%m.%Y").date())
                except ValueError:
                    continue
        
        if not done_dates:
            return 0, 0
            
        done_dates = sorted(list(set(done_dates)))
        
        best_streak = 0
        current_streak = 0
        
        # Считаем все серии в истории для определения лучшей
        temp_streak = 1
        for i in range(1, len(done_dates)):
            if done_dates[i] - done_dates[i-1] == timedelta(days=1):
                temp_streak += 1
            else:
                if temp_streak > best_streak:
                    best_streak = temp_streak
                temp_streak = 1
        if temp_streak > best_streak:
            best_streak = temp_streak

        # Расчет текущей активной серии (которая идет прямо сейчас)
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        
        # Если последний выполненный день не сегодня и не вчера, то текущая серия прервана (0)
        if done_dates[-1] == today or done_dates[-1] == yesterday:
            # Идем с конца назад и считаем дни без перерывов
            curr_temp = 1
            for i in range(len(done_dates) - 1, 0, -1):
                if done_dates[i] - done_dates[i-1] == timedelta(days=1):
                    curr_temp += 1
                else:
                    break
            current_streak = curr_temp
        else:
            current_streak = 0
            
        return current_streak, best_streak

    @staticmethod
    def export_data(filepath):
        data = HabitService.load_data()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def import_data(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                imported = json.load(f)
            if "habits" in imported:
                HabitService.save_data(imported)
                return True
        except Exception:
            pass
        return False