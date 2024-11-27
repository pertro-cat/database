# controller/insert_genre_controller.py

from flask import Blueprint, jsonify
from service.insert_genre_servise import BulkInsertService

bulk_insert_bp = Blueprint('bulk_insert', __name__)

@bulk_insert_bp.route('/insert_noname_genres', methods=['POST'])
def insert_noname_genres():
    response, status_code = BulkInsertService.insert_noname_genres()
    return jsonify(response), status_code
