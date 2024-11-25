# service/userdownload_song_service.py
from extensions import db
from dao.models import UserDownloadHasSong

class UserDownloadSongService:
    
    @staticmethod
    def get_all_records():
        """
        Отримує всі записи з таблиці userdownloads_has_songs.
        
        Повертає:
            list: Список словників, де кожен словник представляє один запис.
        """
        records = UserDownloadHasSong.query.all()
        return [record.to_dict() for record in records]

    @staticmethod
    def get_record(download_id, song_id):
        """
        Отримує один запис за download_id та song_id.

        Параметри:
            download_id (int): Ідентифікатор userdownloads_download_id для запису.
            song_id (int): Ідентифікатор songs_song_id для запису.

        Повертає:
            dict: Словник, що представляє запис, якщо запис знайдено, або None, якщо ні.
        """
        record = UserDownloadHasSong.query.get((download_id, song_id))
        return record.to_dict() if record else None

    @staticmethod
    def create_record(data):
        """
        Створює новий запис у таблиці userdownloads_has_songs.

        Параметри:
            data (dict): Словник, що містить userdownloads_download_id і songs_song_id.

        Повертає:
            dict: Словник, що представляє створений запис.
        """
        # Створюємо новий об'єкт для стикувальної таблиці
        record = UserDownloadHasSong(
            userdownloads_download_id=data.get('userdownloads_download_id'),
            songs_song_id=data.get('songs_song_id')
        )
        # Додаємо новий запис до сесії та зберігаємо
        db.session.add(record)
        db.session.commit()
        return record.to_dict()

    @staticmethod
    def update_record(download_id, song_id, data):
        """
        Оновлює запис у таблиці userdownloads_has_songs, видаляючи старий запис
        і створюючи новий з оновленими значеннями.

        Параметри:
            download_id (int): Ідентифікатор поточного userdownloads_download_id для запису.
            song_id (int): Ідентифікатор поточного songs_song_id для запису.
            data (dict): Нові значення для полів userdownloads_download_id і songs_song_id.

        Повертає:
            dict: Словник, що представляє оновлений запис, або None, якщо початковий запис не знайдено.
        """
        # Пошук запису для оновлення
        record = UserDownloadHasSong.query.get((download_id, song_id))
        if record:
            # Видаляємо старий запис
            db.session.delete(record)
            db.session.commit()

            # Створюємо новий запис із новими значеннями
            new_record = UserDownloadHasSong(
                userdownloads_download_id=data['userdownloads_download_id'],
                songs_song_id=data['songs_song_id']
            )
            db.session.add(new_record)
            db.session.commit()
            return new_record.to_dict()
        return None

    @staticmethod
    def delete_record(download_id, song_id):
        """
        Видаляє запис з таблиці userdownloads_has_songs за download_id та song_id.

        Параметри:
            download_id (int): Ідентифікатор userdownloads_download_id для запису.
            song_id (int): Ідентифікатор songs_song_id для запису.

        Повертає:
            bool: True, якщо запис успішно видалено, або False, якщо запис не знайдено.
        """
        # Пошук запису для видалення
        record = UserDownloadHasSong.query.get((download_id, song_id))
        if record:
            db.session.delete(record)
            db.session.commit()
            return True
        return False