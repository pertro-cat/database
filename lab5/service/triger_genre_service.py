#service/triger_genre_service.py 
from extensions import db
from dao.models import Genre
import traceback

class GenreService:
    @staticmethod
    def add_genre(data):
        """Додає новий жанр до таблиці genres з перевіркою тригера."""
        try:
            # Перевірка значення ranking перед вставкою
            if data['ranking'] % 100 == 0:
                raise ValueError("The 'ranking' value cannot end with two zeros.")
            
            # Створення об'єкта Genre
            new_genre = Genre(
                genre_name=data['genre_name'],
                genre_description=data['genre_description'],
                origin_year=data.get('origin_year'),
                ranking=data['ranking'],
                country_of_genre=data.get('country_of_genre', 'Unknown')
            )

            db.session.add(new_genre)
            db.session.commit()

            return {"message": "Genre added successfully!", "genre_id": new_genre.genre_id}

        except ValueError as e:
            # Логіка обробки помилок валідації
            raise Exception(f"Validation Error: {str(e)}")
        except Exception as e:
            # Логування інших помилок
            error_details = traceback.format_exc()
            print(f"Error while adding genre: {error_details}")
            raise Exception(f"Failed to add genre: {str(e)}")