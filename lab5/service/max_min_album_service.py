# services/max_min_album_service.py

from extensions import db
import traceback  # Для стек-трейсу

from extensions import db
from sqlalchemy.sql import text  # Імпорт функції text
import traceback

class TrackStatsService:
    @staticmethod
    def get_total_tracks_stats(stat_type):
        """Отримати статистику для total_tracks на основі stat_type."""
        
        # Перевірка валідності параметра
        if stat_type not in ['MAX', 'MIN', 'SUM', 'AVG']:
            raise ValueError("Invalid stat_type. Use MAX, MIN, SUM, or AVG.")

        try:
            # Виклик SQL-функції
            query = text("SELECT calculate_total_tracks_stats(:stat_type) AS result")  # Використання text()
            print(f"Executing query: {query}")
            
            # Виконання запиту
            result = db.session.execute(query, {"stat_type": stat_type}).fetchone()
            print(f"Raw query result: {result}")

            # Обробка відсутності результату
            if result is None or result.result is None:
                print("SQL query returned no result or None for result.")
                return None
            
            # Повернення числового значення
            return float(result.result)
        
        except Exception as e:
            # Логування повної інформації про помилку
            error_details = traceback.format_exc()
            print(f"SQL Execution Error: {error_details}")
            raise Exception(f"Database query failed: {str(e)}")
