# controllers/split_users_controller.py


from flask import Blueprint, jsonify
from service.split_users_service import SplitUsersService
import traceback

# Blueprint для маршруту
split_users_bp = Blueprint('split_users', __name__)

@split_users_bp.route('/create/newTable', methods=['POST'])
def create_split_users_tables():
    """Створення таблиць user_part1 та user_part2 через API."""
    try:
        # Виклик сервісу для виконання процедури
        result = SplitUsersService.create_split_users_tables()
        return jsonify(result), 201
    except Exception as e:
        # Обробка помилок
        error_details = traceback.format_exc()
        print(f"Error: {error_details}")
        return jsonify({
            "error": "Failed to create tables.",
            "details": str(e)
        }), 500


