#controller/genre_reviews_controller.py
from flask import Blueprint, request, jsonify
from service.genre_reviews_service import GenreReviewService

genre_reviews_bp = Blueprint('genre_reviews', __name__)

@genre_reviews_bp.route('/reviews', methods=['POST'])
def create_genre_review():
    """Create a new genre review."""
    data = request.get_json()
    return jsonify(*GenreReviewService.create_review(data))

@genre_reviews_bp.route('/reviews', methods=['GET'])
def get_all_genre_reviews():
    """Retrieve all genre reviews."""
    return jsonify(*GenreReviewService.get_all_reviews())

@genre_reviews_bp.route('/reviews/<int:review_id>', methods=['GET'])
def get_genre_review(review_id):
    """Retrieve a genre review by ID."""
    return jsonify(*GenreReviewService.get_review_by_id(review_id))

@genre_reviews_bp.route('/reviews/<int:review_id>', methods=['PUT'])
def update_genre_review(review_id):
    """Update a genre review."""
    data = request.get_json()
    return jsonify(*GenreReviewService.update_review(review_id, data))

@genre_reviews_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_genre_review(review_id):
    """Delete a genre review."""
    return jsonify(*GenreReviewService.delete_review(review_id))
