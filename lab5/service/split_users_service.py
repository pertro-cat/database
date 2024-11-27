# services/split_users_service.py


from extensions import db
import traceback

class SplitUsersService:
    @staticmethod
    def create_split_users_tables():
        """
        Виконання процедури split_users_randomly для створення таблиць user_part1 та user_part2.
        """
        try:
            # Отримання сирого підключення до MySQL
            connection = db.engine.raw_connection()
            cursor = connection.cursor()

            # Виклик процедури
            cursor.callproc("split_users_randomly")

            # Обробка всіх результатів процедури
            for result in cursor.stored_results():
                print(result.fetchall())  # Якщо процедура повертає будь-які дані

            # Закриття курсора і підключення
            cursor.close()
            connection.commit()
            connection.close()

            return {
                "message": "Tables 'user_part1' and 'user_part2' created successfully!"
            }
        except Exception as e:
            # Логування помилки
            error_details = traceback.format_exc()
            print(f"Error while executing split procedure: {error_details}")
            raise Exception(f"Failed to execute procedure: {str(e)}")

