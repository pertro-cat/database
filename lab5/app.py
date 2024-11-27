# app.py

import yaml
from flask import Flask
from extensions import db
from controller.account_controller import account_bp 
from controller.soung_controller import songs_bp      
from controller.playlist_controller import playlists_bp 
from controller.genre_controller import genre_bp 
from controller.favorit_artist_controller import user_favorite_artist_bp  
from controller.user_download_controller import user_download_song_bp
from controller.review_controller import reviews_bp
from controller.genre_reviews_controller import genre_reviews_bp
from controller.param_insert_genre_controller import param_genre_bp
from controller.user_playlists_controller import user_playlist_bp
from controller.insert_genre_controller import bulk_insert_bp
from controller.max_min_album_controller import track_stats_bp
from controller.split_users_controller import split_users_bp
from controller.triger_genre_controller import genre_post_bp

def create_app():
    app = Flask(__name__)

    with open("config/app.yml", "r") as ymlfile:
        config = yaml.safe_load(ymlfile)

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+mysqlconnector://{config['database']['user']}:{config['database']['password']}"
        f"@{config['database']['host']}/{config['database']['database']}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = config['database'].get('secret_key', 'default_secret_key')

    db.init_app(app)

    app.register_blueprint(account_bp, url_prefix='/api')

    app.register_blueprint(songs_bp, url_prefix='/api')

    app.register_blueprint(playlists_bp, url_prefix='/api')

    app.register_blueprint(genre_bp, url_prefix='/api')

    app.register_blueprint(user_favorite_artist_bp, url_prefix='/api')

    app.register_blueprint(user_download_song_bp, url_prefix='/api')

    app.register_blueprint(reviews_bp, url_prefix='/api')
    
    app.register_blueprint(genre_reviews_bp, url_prefix='/api')

    app.register_blueprint(param_genre_bp, url_prefix='/api')

    app.register_blueprint(user_playlist_bp, url_prefix='/api')

    app.register_blueprint(bulk_insert_bp, url_prefix='/api')

    app.register_blueprint(track_stats_bp, url_prefix='/api')

    app.register_blueprint(split_users_bp, url_prefix='/api')

    app.register_blueprint(genre_post_bp, url_prefix='/api')



    @app.route('/')
    def home():
        return 'Flask app is running with config from app.yml!'

    @app.errorhandler(404)
    def not_found_error(error):
        return {'message': 'Resource not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'message': 'Internal server error'}, 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
