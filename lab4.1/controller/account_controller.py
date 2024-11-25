# controller/account_controller.py

from flask import Blueprint, request, jsonify
from service.account_service import AccountService  # Імпорт сервісу

# Створення Blueprint для account контролера
account_bp = Blueprint('account', __name__)

# Маршрути контролера

# Отримання всіх користувачів
@account_bp.route('/accounts', methods=['GET'])
def get_users():
    users = AccountService.get_all_users()
    return jsonify(users), 200

# Отримання користувача за ID
@account_bp.route('/accounts/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = AccountService.get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({'message': 'User not found'}), 404

# Додавання нового користувача
@account_bp.route('/accounts', methods=['POST'])
def add_user():
    data = request.get_json()
    # Перевірка наявності необхідних полів у запиті
    required_fields = ['username', 'email', 'password', 'gender']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400

    user = AccountService.create_user(data)
    return jsonify(user), 201

# Оновлення інформації користувача
@account_bp.route('/accounts/<int:user_id>', methods=['PUT'])
def update_user_info(user_id):
    data = request.get_json()

    # Перевірка коректності значення поля "gender"
    valid_genders = ['M', 'F', 'Other']
    if 'gender' in data and data['gender'] not in valid_genders:
        return jsonify({'message': 'Invalid gender value'}), 400

    updated_user = AccountService.update_user(user_id, data)
    if updated_user:
        return jsonify(updated_user), 200
    return jsonify({'message': 'User not found or failed to update'}), 400

# Видалення користувача
@account_bp.route('/accounts/<int:user_id>', methods=['DELETE'])
def delete_user_account(user_id):
    success = AccountService.delete_user(user_id)
    if success:
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'message': 'User not found or failed to delete'}), 404
