#controllers/param_insert_genre_controller.py
from flask import Blueprint, request, jsonify
from service.param_insert_genre_servise import GenreService

# Унікальна назва Blueprint для параметризованих запитів
param_genre_bp = Blueprint('param_genre', __name__)

@param_genre_bp.route('/param_genres', methods=['POST'])
def create_param_genre():
    data = request.get_json()

    # Перевірка вхідних даних
    if not data:
        return {'message': 'No input data provided'}, 400

    genre_name = data.get('genre_name')
    genre_description = data.get('genre_description')
    origin_year = data.get('origin_year')
    ranking = data.get('ranking')
    country_of_genre = data.get('country_of_genre')

    # Перевірка обов'язкових полів
    if not genre_name or not genre_description or ranking is None:
        return {'message': 'Missing required fields: genre_name, genre_description, or ranking'}, 400

    # Виклик сервісу
    result, status_code = GenreService.add_genre(
        genre_name=genre_name,
        genre_description=genre_description,
        origin_year=origin_year,
        ranking=ranking,
        country_of_genre=country_of_genre
    )

    return jsonify(result), status_code
