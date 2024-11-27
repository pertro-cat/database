#controllers/user_playlists_controller.py
from flask import Blueprint, request, jsonify
from service.user_playlist_service import UserPlaylistService

user_playlist_bp = Blueprint('user_playlists', __name__)

# POST: Додати зв'язок між користувачем і плейлистом
@user_playlist_bp.route('/user_playlists', methods=['POST'])
def add_user_playlist():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    username = data.get('username')
    playlist_name = data.get('playlist_name')

    if not username or not playlist_name:
        return jsonify({'message': 'Missing required fields'}), 400

    result, status_code = UserPlaylistService.link_user_to_playlist(username, playlist_name)
    return jsonify(result), status_code


# GET: Отримати всі зв'язки між користувачами та плейлистами
@user_playlist_bp.route('/user_playlists', methods=['GET'])
def get_user_playlists():
    links = UserPlaylistService.get_user_playlists()
    return jsonify(links), 200
