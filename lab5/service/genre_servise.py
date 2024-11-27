#service/genre_service.py
from sqlalchemy.sql import text  # Для роботи з текстовими SQL запитами
from dao.models import db, Genre


class GenreService:
    @staticmethod
    def create_genre(data):
        """Create a new genre in the database."""
        required_fields = ['genre_name', 'genre_description', 'origin_year', 'ranking', 'country_of_genre']
        if not all(field in data for field in required_fields):
            return {'error': 'Missing required fields'}, 400

        try:
            new_genre = Genre(
                genre_name=data['genre_name'],
                genre_description=data['genre_description'],
                origin_year=data['origin_year'],
                ranking=data['ranking'],
                country_of_genre=data['country_of_genre']
            )

            db.session.add(new_genre)
            db.session.commit()
            return new_genre.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create genre: {str(e)}'}, 500

    @staticmethod
    def get_all_genres():
        """Retrieve all genres from the database."""
        try:
            genres = Genre.query.all()
            return [genre.to_dict() for genre in genres], 200
        except Exception as e:
            return {'error': f'Failed to retrieve genres: {str(e)}'}, 500

    @staticmethod
    def get_genre_by_id(genre_id):
        """Retrieve a genre by its ID."""
        try:
            genre = Genre.query.get(genre_id)
            if not genre:
                return {'error': 'Genre not found'}, 404
            return genre.to_dict(), 200
        except Exception as e:
            return {'error': f'Failed to retrieve genre by ID: {str(e)}'}, 500

    @staticmethod
    def update_genre(genre_id, data):
        """Update genre details by ID."""
        try:
            genre = Genre.query.get(genre_id)
            if not genre:
                return {'error': 'Genre not found'}, 404

            # Update fields if they are provided in the data
            genre.genre_name = data.get('genre_name', genre.genre_name)
            genre.genre_description = data.get('genre_description', genre.genre_description)
            genre.origin_year = data.get('origin_year', genre.origin_year)
            genre.ranking = data.get('ranking', genre.ranking)
            genre.country_of_genre = data.get('country_of_genre', genre.country_of_genre)

            db.session.commit()
            return genre.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to update genre: {str(e)}'}, 500

    @staticmethod
    def delete_genre_and_get_logs(genre_id):
        """Delete a genre by its ID and fetch logs from genres_log."""
        try:
            genre = Genre.query.get(genre_id)
            if not genre:
                return {'error': 'Genre not found'}, 404

            # Видалення жанру
            db.session.delete(genre)
            db.session.commit()

            # Отримання записів з таблиці genres_log
            query = text("SELECT * FROM genres_log WHERE genre_id = :genre_id ORDER BY deleted_at DESC")
            logs = db.session.execute(query, {'genre_id': genre_id}).fetchall()

            # Форматування даних для відповіді
            logs_result = [
                {
                    'log_id': log.log_id,
                    'genre_id': log.genre_id,
                    'genre_name': log.genre_name,
                    'genre_description': log.genre_description,
                    'origin_year': log.origin_year,
                    'ranking': log.ranking,
                    'country_of_genre': log.country_of_genre,
                    'deleted_at': log.deleted_at.strftime('%Y-%m-%d %H:%M:%S')
                }
                for log in logs
            ]

            return {
                'message': 'Genre deleted successfully',
                'logs': logs_result
            }, 200

        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to delete genre and fetch logs: {str(e)}'}, 500
