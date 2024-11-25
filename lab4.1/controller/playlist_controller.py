# controller/playlist_controller.py

from flask import Blueprint, jsonify, request
from service.playlist_servise import PlaylistService  # Імпорт PlaylistService

# Ініціалізація Blueprint для плейлистів
playlists_bp = Blueprint('playlists', __name__)

# Створення нового плейлиста
@playlists_bp.route('/playlists', methods=['POST'])
def create_playlist():
    data = request.json
    result, status_code = PlaylistService.create_playlist(data)
    return jsonify(result), status_code

# Отримання інформації про всі плейлисти
@playlists_bp.route('/playlists', methods=['GET'])
def get_playlists():
    playlists, status_code = PlaylistService.get_all_playlists()
    return jsonify(playlists), status_code

# Отримання інформації про конкретний плейлист за ID
@playlists_bp.route('/playlists/<int:playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    result, status_code = PlaylistService.get_playlist_by_id(playlist_id)
    return jsonify(result), status_code

# Оновлення інформації про плейлист за ID
@playlists_bp.route('/playlists/<int:playlist_id>', methods=['PUT'])
def update_playlist(playlist_id):
    data = request.json
    result, status_code = PlaylistService.update_playlist(playlist_id, data)
    return jsonify(result), status_code

# Видалення плейлиста за ID
@playlists_bp.route('/playlists/<int:playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    result, status_code = PlaylistService.delete_playlist(playlist_id)
    return jsonify(result), status_code
