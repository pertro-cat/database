from flask import Blueprint, request, jsonify
from service.triger_genre_service import GenreService
import traceback

# Створення Blueprint для маршруту
genre_post_bp = Blueprint('triger_genres', __name__)

@genre_post_bp.route('/trigerGenres', methods=['POST'])
def add_genre_with_trigger():
    """Обробляє POST-запит для додавання нового жанру з перевіркою тригера."""
    try:
        # Отримання даних із запиту
        data = request.get_json()

        # Перевірка обов'язкових полів
        if 'genre_name' not in data or 'genre_description' not in data or 'ranking' not in data:
            return jsonify({"error": "Fields 'genre_name', 'genre_description', and 'ranking' are required."}), 400

        # Виклик сервісу для додавання жанру
        result = GenreService.add_genre(data)
        return jsonify(result), 201

    except Exception as e:
        # Логування та обробка помилок
        error_details = traceback.format_exc()
        print(f"Error while adding genre: {error_details}")
        return jsonify({
            "error": "Failed to add genre.",
            "details": str(e)
        }), 500
