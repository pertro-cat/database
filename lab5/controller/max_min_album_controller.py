# controllers/max_min_album_controller.py
from flask import Blueprint, jsonify, request
from service.max_min_album_service import TrackStatsService
import traceback  # Доданий імпорт

track_stats_bp = Blueprint('track_stats', __name__)

@track_stats_bp.route('/track-stats', methods=['GET'])
def get_track_stats():
    """Обробка GET-запиту для отримання статистики."""
    stat_type = request.args.get('stat_type')  # Отримати параметр stat_type
    print(f"Received stat_type: {stat_type}")

    # Перевірка наявності параметра stat_type
    if not stat_type:
        return jsonify({"error": "Parameter 'stat_type' is required"}), 400

    try:
        # Отримання статистики за допомогою сервісу
        result = TrackStatsService.get_total_tracks_stats(stat_type)
        
        # Якщо дані відсутні
        if result is None:
            return jsonify({"error": "No data found"}), 404
        
        # Успішна відповідь
        return jsonify({"stat_type": stat_type, "value": result}), 200

    except ValueError as e:
        print(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        # Логування внутрішньої помилки з повним стек-трейсом
        error_details = traceback.format_exc()
        print(f"Internal server error: {error_details}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
