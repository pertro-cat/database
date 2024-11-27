# controller/songs_controller.py

from flask import Blueprint, jsonify, request
from service.song_servise import SongService  # Імпорт SongService

# Ініціалізація Blueprint для пісень
songs_bp = Blueprint('songs', __name__)

# Створення нової пісні
@songs_bp.route('/songs', methods=['POST'])
def create_song():
    data = request.json
    result, status_code = SongService.create_song(data)
    return jsonify(result), status_code

# Отримання інформації про всі пісні
@songs_bp.route('/songs', methods=['GET'])
def get_songs():
    songs = SongService.get_all_songs()
    return jsonify(songs)

# Отримання інформації про конкретну пісню за ID
@songs_bp.route('/songs/<int:song_id>', methods=['GET'])
def get_song(song_id):
    result, status_code = SongService.get_song_by_id(song_id)
    return jsonify(result), status_code

# Оновлення інформації про пісню за ID
@songs_bp.route('/songs/<int:song_id>', methods=['PUT'])
def update_song(song_id):
    data = request.json
    result, status_code = SongService.update_song(song_id, data)
    return jsonify(result), status_code

# Видалення пісні за ID
@songs_bp.route('/songs/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    result, status_code = SongService.delete_song(song_id)
    return jsonify(result), status_code
