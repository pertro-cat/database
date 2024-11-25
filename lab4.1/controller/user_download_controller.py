from flask import Blueprint, request, jsonify
from service.userdownload_song_service import UserDownloadSongService
from sqlalchemy.orm import joinedload
from dao.models import UserDownloadHasSong, Song, UserDownload  # Імпортуйте потрібні моделі

user_download_song_bp = Blueprint('user_download_song_bp', __name__)

# Отримати всі записи (GET)
@user_download_song_bp.route('/userdownloads_has_songs', methods=['GET'])
def get_all_user_downloads_songs():
    """Отримує всі записи з таблиці userdownloads_has_songs."""
    records = UserDownloadSongService.get_all_records()
    return jsonify(records), 200


# Отримати запис за download_id та song_id (GET)
@user_download_song_bp.route('/userdownloads_has_songs/<int:download_id>/<int:song_id>', methods=['GET'])
def get_user_download_song(download_id, song_id):
    """
    Отримує конкретний запис за download_id та song_id або детальні дані з таблиці songs та downloads.
    """
    # Спроба отримати детальні дані про пісню та завантаження
    record = UserDownloadHasSong.query.filter_by(
        userdownloads_download_id=download_id,
        songs_song_id=song_id
    ).join(
        Song, UserDownloadHasSong.songs_song_id == Song.song_id
    ).join(
        UserDownload, UserDownloadHasSong.userdownloads_download_id == UserDownload.download_id
    ).add_columns(
        Song.song_title, Song.genre_id, Song.duraction, Song.realease_date,
        UserDownload.device_type, UserDownload.operating_system, UserDownload.location
    ).first()

    # Якщо знайдено пов'язані дані
    if record:
        response = {
            "userdownloads_download_id": download_id,
            "songs_song_id": song_id,
            "song_details": {
                "title": record.song_title,
                "genre_id": record.genre_id,
                "duraction": str(record.duraction),
                "realease_date": str(record.realease_date)
            },
            "download_details": {
                "device_type": record.device_type,
                "operating_system": record.operating_system,
                "location": record.location
            }
        }
        return jsonify(response), 200

    # Якщо пов'язаних даних немає, повернути базовий запис
    basic_record = UserDownloadSongService.get_record(download_id, song_id)
    if basic_record:
        return jsonify(basic_record), 200

    # У випадку, якщо запис не знайдено
    return jsonify({"error": "Record not found"}), 404


# Створити новий запис (POST)
@user_download_song_bp.route('/userdownloads_has_songs', methods=['POST'])
def create_user_download_song():
    """Створює новий запис у таблиці userdownloads_has_songs."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    record = UserDownloadSongService.create_record(data)
    return jsonify(record), 201


# Оновити запис за download_id та song_id (PUT)
@user_download_song_bp.route('/userdownloads_has_songs/<int:download_id>/<int:song_id>', methods=['PUT'])
def update_user_download_song(download_id, song_id):
    """Оновлює існуючий запис за download_id та song_id."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    updated_record = UserDownloadSongService.update_record(download_id, song_id, data)
    if updated_record:
        return jsonify(updated_record), 200
    return jsonify({"error": "Record not found"}), 404


# Видалити запис за download_id та song_id (DELETE)
@user_download_song_bp.route('/userdownloads_has_songs/<int:download_id>/<int:song_id>', methods=['DELETE'])
def delete_user_download_song(download_id, song_id):
    """Видаляє запис з таблиці userdownloads_has_songs за download_id та song_id."""
    success = UserDownloadSongService.delete_record(download_id, song_id)
    if success:
        return jsonify({"message": "Record deleted"}), 200
    return jsonify({"error": "Record not found"}), 404
