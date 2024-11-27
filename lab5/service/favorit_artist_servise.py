from dao.models import db, UserFavoriteArtist

class UserFavoriteArtistService:
    
    @staticmethod
    def create_favorite(user_id, author_id, added_date, comment=None, listen_count=0, last_listen_date=None):
        """Створює новий запис про улюбленого артиста користувача."""
        new_favorite = UserFavoriteArtist(
            user_id=user_id,
            author_id=author_id,
            added_date=added_date,
            comment=comment,
            listen_count=listen_count,
            last_listen_date=last_listen_date
        )
        db.session.add(new_favorite)
        db.session.commit()
        return new_favorite.to_dict()

    @staticmethod
    def get_favorite_by_id(favorite_id):
        """Отримує запис про улюбленого артиста за його ID."""
        favorite = UserFavoriteArtist.query.get(favorite_id)
        return favorite.to_dict() if favorite else None

    @staticmethod
    def get_all_favorites():
        """Отримує всі записи про улюблених артистів."""
        favorites = UserFavoriteArtist.query.all()
        return [favorite.to_dict() for favorite in favorites]

    @staticmethod
    def update_favorite(favorite_id, **kwargs):
        """
        Оновлює існуючий запис про улюбленого артиста.
        :param kwargs: Поля для оновлення, наприклад, comment, listen_count тощо.
        """
        favorite = UserFavoriteArtist.query.get(favorite_id)
        if not favorite:
            return None
        for key, value in kwargs.items():
            if hasattr(favorite, key):
                setattr(favorite, key, value)
        db.session.commit()
        return favorite.to_dict()

    @staticmethod
    def delete_favorite(favorite_id):
        """Видаляє запис про улюбленого артиста за його ID."""
        favorite = UserFavoriteArtist.query.get(favorite_id)
        if not favorite:
            return False
        db.session.delete(favorite)
        db.session.commit()
        return True
