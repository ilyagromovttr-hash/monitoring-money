import unittest
from core.habit_service import HabitService

class TestHabitTracker(unittest.TestCase):
    def test_empty_history_streaks(self):
        """Проверка пустой истории"""
        curr, best = HabitService.calculate_streaks({})
        self.assertEqual(curr, 0)
        self.assertEqual(best, 0)

    def test_single_done_streak(self):
        """Проверка серии из одного (сегодняшнего) дня"""
        from datetime import datetime
        today_str = datetime.now().strftime("%d.%m.%Y")
        history = {today_str: "done"}
        
        curr, best = HabitService.calculate_streaks(history)
        self.assertEqual(curr, 1)
        self.assertEqual(best, 1)

    def test_broken_streak(self):
        """Проверка прерванной серии"""
        history = {
            "01.06.2026": "done",
            "02.06.2026": "done",
            "03.06.2026": "skipped"
        }
        curr, best = HabitService.calculate_streaks(history)
        self.assertEqual(curr, 0) # Текущая серия прервана
        self.assertEqual(best, 2) # Лучшая серия была 2 дня

if __name__ == "__main__":
    unittest.main()