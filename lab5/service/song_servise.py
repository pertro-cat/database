#servise/song_servise.py
from dao.models import db, Song
from flask import jsonify

class SongService:
    @staticmethod
    def create_song(data):
        """Create a new song in the database."""
        required_fields = ['song_title', 'genre_id', 'author_id', 'price', 'duraction', 'realese_date']
        
        # Check if all required fields are present in the input data
        if not all(field in data for field in required_fields):
            return {'error': 'Missing required fields'}, 400

        # Create a new song record with provided data
        new_song = Song(
            song_title=data['song_title'],
            genre_id=data['genre_id'],
            author_id=data['author_id'],
            album_id=data.get('album_id'),
            label_id=data.get('label_id'),
            price=data['price'],
            download_count=data.get('download_count', 0),
            duraction=data['duraction'],  # Use 'duraction' as per model definition
            realese_date=data['realese_date'],  # Use 'realese_date' as per model definition
            text_of_song=data.get('text_of_song', ''),
            downloads=data.get('downloads', 0)
        )

        # Add and commit the new song to the database
        db.session.add(new_song)
        db.session.commit()
        
        return new_song.to_dict(), 201

    @staticmethod
    def get_all_songs():
        """Retrieve all songs from the database."""
        songs = Song.query.all()
        return [song.to_dict() for song in songs], 200

    @staticmethod
    def get_song_by_id(song_id):
        """Retrieve a song by its ID."""
        song = Song.query.get(song_id)
        if not song:
            return {'error': 'Song not found'}, 404
        return song.to_dict(), 200

    @staticmethod
    def update_song(song_id, data):
        """Update song details by ID."""
        song = Song.query.get(song_id)
        if not song:
            return {'error': 'Song not found'}, 404

        # Update fields if they are provided in the input data
        song.song_title = data.get('song_title', song.song_title)
        song.genre_id = data.get('genre_id', song.genre_id)
        song.author_id = data.get('author_id', song.author_id)
        song.album_id = data.get('album_id', song.album_id)
        song.label_id = data.get('label_id', song.label_id)
        song.price = data.get('price', song.price)
        song.download_count = data.get('download_count', song.download_count)
        song.duraction = data.get('duraction', song.duraction)  # Use 'duraction' as per model definition
        song.realese_date = data.get('realese_date', song.realese_date)  # Use 'realese_date' as per model definition
        song.text_of_song = data.get('text_of_song', song.text_of_song)
        song.downloads = data.get('downloads', song.downloads)

        # Commit the updates to the database
        db.session.commit()
        
        return song.to_dict(), 200

    @staticmethod
    def delete_song(song_id):
        """Delete a song by its ID."""
        song = Song.query.get(song_id)
        if not song:
            return {'error': 'Song not found'}, 404

        # Delete the song and commit the changes
        db.session.delete(song)
        db.session.commit()
        
        return {'message': 'Song deleted successfully'}, 200
