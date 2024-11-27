from extensions import db
from dao.models import Review, Song, User


class ReviewService:
    @staticmethod
    def add_review(data):
        """
        Додає новий відгук у базу даних.
        Перевіряє існування song_id і user_id перед створенням.
        """
        song_id = data.get('song_id')
        user_id = data.get('user_id')
        review_text = data.get('review_text')
        rating = data.get('rating')

        # Перевірка обов’язкових полів
        if not song_id or not user_id or not rating:
            return {'error': 'Missing required fields: song_id, user_id, or rating'}, 400

        # Перевірка наявності пісні
        if not db.session.query(db.exists().where(Song.song_id == song_id)).scalar():
            return {'error': 'Song ID does not exist'}, 400

        # Перевірка наявності користувача
        if not db.session.query(db.exists().where(User.user_id == user_id)).scalar():
            return {'error': 'User ID does not exist'}, 400

        # Перевірка діапазону оцінки
        if not (1 <= rating <= 5):
            return {'error': 'Rating must be between 1 and 5'}, 400

        # Створення нового відгуку
        new_review = Review(
            song_id=song_id,
            user_id=user_id,
            review_text=review_text,
            rating=rating
        )
        db.session.add(new_review)
        db.session.commit()
        return {'message': 'Review added successfully'}, 201

    @staticmethod
    def get_all_reviews():
        """
        Повертає всі відгуки у вигляді списку JSON-об’єктів.
        """
        reviews = Review.query.all()
        return [review.to_dict() for review in reviews], 200

    @staticmethod
    def get_review_by_id(review_id):
        """
        Повертає конкретний відгук за його ID.
        """
        review = Review.query.get(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @staticmethod
    def delete_review(review_id):
        """
        Видаляє відгук за його ID.
        """
        review = Review.query.get(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        db.session.delete(review)
        db.session.commit()
        return {'message': 'Review deleted successfully'}, 200

    @staticmethod
    def update_review(review_id, data):
        """
        Оновлює текст та оцінку відгуку за його ID.
        """
        review = Review.query.get(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        review_text = data.get('review_text')
        rating = data.get('rating')

        if review_text:
            review.review_text = review_text
        if rating:
            if not (1 <= rating <= 5):
                return {'error': 'Rating must be between 1 and 5'}, 400
            review.rating = rating

        db.session.commit()
        return {'message': 'Review updated successfully'}, 200
