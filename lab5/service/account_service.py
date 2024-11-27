# service/account_service.py

from extensions import db
from dao.models import User


class AccountService:
    @staticmethod
    def get_all_users():
        """
        Отримує всіх користувачів з бази даних.
        """
        users = User.query.all()
        # Повертає список користувачів у форматі словників для зручної конвертації у JSON
        return [user.to_dict() for user in users]

    @staticmethod
    def get_user_by_id(user_id):
        """
        Отримує користувача за його ID.
        """
        user = User.query.get(user_id)
        # Якщо користувач знайдений, повертає його у форматі словника, інакше повертає None
        return user.to_dict() if user else None

    @staticmethod
    def create_user(data):
        """
        Створює нового користувача на основі наданих даних.
        """
        # Перевірка наявності допустимих значень для username
        valid_usernames = ['svitlana', 'petro', 'olha', 'taras']
        if data.get('username') not in valid_usernames:
            raise ValueError("Invalid username. Allowed values are: 'svitlana', 'petro', 'olha', 'taras'.")

        # Створюємо об'єкт User з даними, переданими у запиті
        user = User(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            gender=data.get('gender'),
            birthdayDate=data.get('birthdayDate')
        )
        # Додаємо нового користувача в сесію та зберігаємо зміни
        db.session.add(user)
        db.session.commit()
        # Повертаємо створеного користувача у форматі словника
        return user.to_dict()

    @staticmethod
    def update_user(user_id, data):
        """
        Оновлює дані користувача за його ID.
        """
        # Отримуємо користувача за ID
        user = User.query.get(user_id)
        if user:
            # Оновлюємо поля користувача, якщо вони передані в запиті
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.password = data.get('password', user.password)
            user.gender = data.get('gender', user.gender)
            user.birthdayDate = data.get('birthdayDate', user.birthdayDate)
            # Зберігаємо зміни
            db.session.commit()
            # Повертаємо оновленого користувача у форматі словника
            return user.to_dict()
        return None

    @staticmethod
    def delete_user(user_id):
        """
        Видаляє користувача за його ID.
        """
        # Отримуємо користувача за ID
        user = User.query.get(user_id)
        if user:
            # Видаляємо користувача з сесії та зберігаємо зміни
            db.session.delete(user)
            db.session.commit()
            return True
        return False
