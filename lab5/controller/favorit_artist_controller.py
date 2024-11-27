from flask import Blueprint, jsonify, request
from service.favorit_artist_servise import UserFavoriteArtistService

# Створення Blueprint для контролера
user_favorite_artist_bp = Blueprint('user_favorite_artist', __name__)

@user_favorite_artist_bp.route('/favorites', methods=['POST'])
def create_favorite():
    """Створення нового запису про улюбленого артиста."""
    data = request.get_json()
    user_id = data.get('user_id')
    author_id = data.get('author_id')
    added_date = data.get('added_date')
    comment = data.get('comment', None)
    listen_count = data.get('listen_count', 0)
    last_listen_date = data.get('last_listen_date', None)
    
    new_favorite = UserFavoriteArtistService.create_favorite(
        user_id=user_id,
        author_id=author_id,
        added_date=added_date,
        comment=comment,
        listen_count=listen_count,
        last_listen_date=last_listen_date
    )
    return jsonify(new_favorite), 201

@user_favorite_artist_bp.route('/favorites/<int:favorite_id>', methods=['GET'])
def get_favorite(favorite_id):
    """Отримання запису про улюбленого артиста за ID."""
    favorite = UserFavoriteArtistService.get_favorite_by_id(favorite_id)
    if favorite:
        return jsonify(favorite), 200
    return jsonify({'message': 'Favorite artist not found'}), 404

@user_favorite_artist_bp.route('/favorites', methods=['GET'])
def get_all_favorites():
    """Отримання всіх записів про улюблених артистів."""
    favorites = UserFavoriteArtistService.get_all_favorites()
    return jsonify(favorites), 200

@user_favorite_artist_bp.route('/favorites/<int:favorite_id>', methods=['PUT'])
def update_favorite(favorite_id):
    """Оновлення запису про улюбленого артиста за ID."""
    data = request.get_json()
    updated_favorite = UserFavoriteArtistService.update_favorite(favorite_id, **data)
    if updated_favorite:
        return jsonify(updated_favorite), 200
    return jsonify({'message': 'Favorite artist not found'}), 404

@user_favorite_artist_bp.route('/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    """Видалення запису про улюбленого артиста за ID."""
    if UserFavoriteArtistService.delete_favorite(favorite_id):
        return jsonify({'message': 'Favorite artist deleted successfully'}), 200
    return jsonify({'message': 'Favorite artist not found'}), 404
