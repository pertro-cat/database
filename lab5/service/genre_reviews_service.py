from dao.models import GenreReview, db
from sqlalchemy.exc import SQLAlchemyError

class GenreReviewService:
    @staticmethod
    def create_review(data):
        """Create a new genre review."""
        try:
            new_review = GenreReview(
                genre_id=data['genre_id'],
                review_text=data['review_text'],
                rating=data['rating']
            )
            db.session.add(new_review)
            db.session.commit()
            return new_review.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': str(e)}, 400

    @staticmethod
    def get_all_reviews():
        """Retrieve all genre reviews."""
        try:
            reviews = GenreReview.query.all()
            return [review.to_dict() for review in reviews], 200
        except SQLAlchemyError as e:
            return {'message': str(e)}, 400

    @staticmethod
    def get_review_by_id(review_id):
        """Retrieve a single genre review by ID."""
        try:
            review = GenreReview.query.get(review_id)
            if not review:
                return {'message': 'Review not found'}, 404
            return review.to_dict(), 200
        except SQLAlchemyError as e:
            return {'message': str(e)}, 400

    @staticmethod
    def update_review(review_id, data):
        """Update an existing genre review."""
        try:
            review = GenreReview.query.get(review_id)
            if not review:
                return {'message': 'Review not found'}, 404
            
            review.review_text = data.get('review_text', review.review_text)
            review.rating = data.get('rating', review.rating)

            db.session.commit()
            return review.to_dict(), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': str(e)}, 400

    @staticmethod
    def delete_review(review_id):
        """Delete a genre review."""
        try:
            review = GenreReview.query.get(review_id)
            if not review:
                return {'message': 'Review not found'}, 404

            db.session.delete(review)
            db.session.commit()
            return {'message': 'Review deleted successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': str(e)}, 400
