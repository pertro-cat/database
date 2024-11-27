# service/playlist_service.py

from dao.models import db, Playlist
from flask import jsonify

class PlaylistService:
    @staticmethod
    def create_playlist(data):
        """Create a new playlist in the database."""
        required_fields = ['playlist_name', 'user_id', 'song_id']
        if not all(field in data for field in required_fields):
            return {'error': 'Missing required fields'}, 400

        new_playlist = Playlist(
            playlist_name=data['playlist_name'],
            user_id=data['user_id'],
            song_id=data['song_id'],
            description=data.get('description', ''),
            name_user_who_create=data.get('name_user_who_create', ''),
            count_of_song=data.get('count_of_song', 0),
            total_duraction=data.get('total_duraction')
        )

        db.session.add(new_playlist)
        db.session.commit()
        return new_playlist.to_dict(), 201

    @staticmethod
    def get_all_playlists():
        """Retrieve all playlists from the database."""
        playlists = Playlist.query.all()
        return [playlist.to_dict() for playlist in playlists], 200

    @staticmethod
    def get_playlist_by_id(playlist_id):
        """Retrieve a playlist by its ID."""
        playlist = Playlist.query.get(playlist_id)
        if not playlist:
            return {'error': 'Playlist not found'}, 404
        return playlist.to_dict(), 200

    @staticmethod
    def update_playlist(playlist_id, data):
        """Update playlist details by ID."""
        playlist = Playlist.query.get(playlist_id)
        if not playlist:
            return {'error': 'Playlist not found'}, 404

        # Update fields if they are provided in the data
        playlist.playlist_name = data.get('playlist_name', playlist.playlist_name)
        playlist.user_id = data.get('user_id', playlist.user_id)
        playlist.song_id = data.get('song_id', playlist.song_id)
        playlist.description = data.get('description', playlist.description)
        playlist.name_user_who_create = data.get('name_user_who_create', playlist.name_user_who_create)
        playlist.count_of_song = data.get('count_of_song', playlist.count_of_song)
        playlist.total_duraction = data.get('total_duraction', playlist.total_duraction)

        db.session.commit()
        return playlist.to_dict(), 200

    @staticmethod
    def delete_playlist(playlist_id):
        """Delete a playlist by its ID."""
        playlist = Playlist.query.get(playlist_id)
        if not playlist:
            return {'error': 'Playlist not found'}, 404

        db.session.delete(playlist)
        db.session.commit()
        return {'message': 'Playlist deleted successfully'}, 200
