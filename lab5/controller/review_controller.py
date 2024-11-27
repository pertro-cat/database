from flask import Blueprint, request, jsonify
from service.review_service import ReviewService

# Ініціалізація Blueprint
reviews_bp = Blueprint('reviews', __name__)

# CRUD операції

@reviews_bp.route('/reviews1', methods=['POST'])
def add_review():
    """
    Створення нового відгуку.
    """
    data = request.get_json()  # Отримання даних із запиту
    result, status_code = ReviewService.add_review(data)
    return jsonify(result), status_code


@reviews_bp.route('/reviews1', methods=['GET'])
def get_all_reviews():
    """
    Отримання всіх відгуків.
    """
    result, status_code = ReviewService.get_all_reviews()
    return jsonify(result), status_code


@reviews_bp.route('/reviews1/<int:review_id>', methods=['GET'])
def get_review_by_id(review_id):
    """
    Отримання конкретного відгуку за його ID.
    """
    result, status_code = ReviewService.get_review_by_id(review_id)
    return jsonify(result), status_code


@reviews_bp.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Оновлення відгуку за його ID.
    """
    data = request.get_json()  # Отримання даних із запиту
    result, status_code = ReviewService.update_review(review_id, data)
    return jsonify(result), status_code


@reviews_bp.route('/reviews1/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Видалення відгуку за його ID.
    """
    result, status_code = ReviewService.delete_review(review_id)
    return jsonify(result), status_code
