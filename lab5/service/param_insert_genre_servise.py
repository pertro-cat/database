#service/param_insert_genre_servise.py
from dao.models import Genre
from extensions import db

class GenreService:
    @staticmethod
    def add_genre(genre_name, genre_description, origin_year, ranking, country_of_genre):
        try:
            # Створення нового жанру
            new_genre = Genre(
                genre_name=genre_name,
                genre_description=genre_description,
                origin_year=origin_year,
                ranking=ranking,
                country_of_genre=country_of_genre
            )
            db.session.add(new_genre)
            db.session.commit()
            return {'message': 'Genre added successfully', 'genre': new_genre.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'Failed to add genre', 'error': str(e)}, 500
