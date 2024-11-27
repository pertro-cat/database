#service/insert_genre_service.py
from dao.models import Genre
from extensions import db

class BulkInsertService:
    @staticmethod
    def insert_noname_genres():
        try:
            base_origin_year = 2000
            base_ranking = 10
            genres_to_insert = []

            for i in range(1, 11):
                genre = Genre(
                    genre_name=f"Noname{i}",
                    genre_description=f"Description for Noname{i}",
                    origin_year=base_origin_year + i,
                    ranking=base_ranking + i,
                    country_of_genre="Unknown"
                )
                genres_to_insert.append(genre)

            db.session.bulk_save_objects(genres_to_insert)
            db.session.commit()

            return {"message": "10 genres inserted successfully"}, 201

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
