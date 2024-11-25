# controller/genre_controller.py

from flask import Blueprint, jsonify, request
from service.genre_servise import GenreService

# Ініціалізація Blueprint для жанрів
genre_bp = Blueprint('genres', __name__)

# Маршрут для створення нового жанру
@genre_bp.route('/genres', methods=['POST'])
def create_genre():
    data = request.json
    result, status_code = GenreService.create_genre(data)
    return jsonify(result), status_code

# Маршрут для отримання всіх жанрів
@genre_bp.route('/genres', methods=['GET'])
def get_all_genres():
    genres, status_code = GenreService.get_all_genres()
    return jsonify(genres), status_code

# Маршрут для отримання жанру за ID
@genre_bp.route('/genres/<int:genre_id>', methods=['GET'])
def get_genre_by_id(genre_id):
    result, status_code = GenreService.get_genre_by_id(genre_id)
    return jsonify(result), status_code

# Маршрут для оновлення жанру за ID
@genre_bp.route('/genres/<int:genre_id>', methods=['PUT'])
def update_genre(genre_id):
    data = request.json
    result, status_code = GenreService.update_genre(genre_id, data)
    return jsonify(result), status_code

# Маршрут для видалення жанру за ID
@genre_bp.route('/genres/<int:genre_id>', methods=['DELETE'])
def delete_genre(genre_id):
    result, status_code = GenreService.delete_genre(genre_id)
    return jsonify(result), status_code
