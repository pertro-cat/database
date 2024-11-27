#service/user_playlist_service.py
from dao.models import User, Playlist, UserPlaylist
from extensions import db


class UserPlaylistService:

    @staticmethod
    def link_user_to_playlist(username, playlist_name):
        """Зв'язати користувача з плейлистом."""
        # Знайти користувача за username
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User not found'}, 404

        # Знайти плейлист за назвою
        playlist = Playlist.query.filter_by(playlist_name=playlist_name).first()
        if not playlist:
            return {'message': 'Playlist not found'}, 404

        # Перевірити, чи запис уже існує
        existing_link = UserPlaylist.query.filter_by(user_id=user.user_id, playlist_id=playlist.playlist_id).first()
        if existing_link:
            return {'message': 'Link already exists'}, 400

        # Додати запис у стикувальну таблицю
        user_playlist = UserPlaylist(user_id=user.user_id, playlist_id=playlist.playlist_id)
        db.session.add(user_playlist)
        db.session.commit()
        return {'message': 'Link created successfully'}, 201

    @staticmethod
    def get_user_playlists():
        """Отримати всі зв'язки між користувачами та плейлистами."""
        links = UserPlaylist.query.all()
        return [link.to_dict() for link in links]
