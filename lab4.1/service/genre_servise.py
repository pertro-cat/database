# service/genre_service.py

from dao.models import db, Genre

class GenreService:
    @staticmethod
    def create_genre(data):
        """Create a new genre in the database."""
        required_fields = ['genre_name', 'genre_description', 'origin_year', 'ranking', 'country_of_genre']
        if not all(field in data for field in required_fields):
            return {'error': 'Missing required fields'}, 400

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

    @staticmethod
    def get_all_genres():
        """Retrieve all genres from the database."""
        genres = Genre.query.all()
        return [genre.to_dict() for genre in genres], 200

    @staticmethod
    def get_genre_by_id(genre_id):
        """Retrieve a genre by its ID."""
        genre = Genre.query.get(genre_id)
        if not genre:
            return {'error': 'Genre not found'}, 404
        return genre.to_dict(), 200

    @staticmethod
    def update_genre(genre_id, data):
        """Update genre details by ID."""
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

    @staticmethod
    def delete_genre(genre_id):
        """Delete a genre by its ID."""
        genre = Genre.query.get(genre_id)
        if not genre:
            return {'error': 'Genre not found'}, 404

        db.session.delete(genre)
        db.session.commit()
        return {'message': 'Genre deleted successfully'}, 200
