-- Task1 --------------------------------------------------------------------------------------------------------------------------
CREATE TABLE genre_reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY, -- Унікальний ідентифікатор відгуку
    genre_id INT NOT NULL,                    -- Ідентифікатор жанру
    review_text TEXT NOT NULL,                -- Текст відгуку
    rating INT CHECK (rating BETWEEN 1 AND 5), -- Рейтинг (від 1 до 5)
    review_date DATETIME DEFAULT CURRENT_TIMESTAMP -- Дата створення відгуку
);

DELIMITER $$

CREATE TRIGGER check_genre_exists
BEFORE INSERT ON genre_reviews
FOR EACH ROW
BEGIN
    IF NOT EXISTS (SELECT 1 FROM genres WHERE genre_id = NEW.genre_id) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Genre ID does not exist in genres table';
    END IF;
END$$

DELIMITER ;

DELIMITER $$


-- Task2 a -- ------------------------------------------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS insert_genre;

DELIMITER $$

CREATE PROCEDURE insert_genre(
    IN p_genre_name VARCHAR(50),
    IN p_genre_description VARCHAR(255),
    IN p_origin_year YEAR,
    IN p_ranking INT,
    IN p_country_of_genre VARCHAR(50)
)
BEGIN
    -- Перевірка, чи не існує жанр із таким самим ім'ям
    IF EXISTS (SELECT 1 FROM genres WHERE genre_name = p_genre_name) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Genre with the same name already exists';
    END IF;

    -- Вставка нового запису
    INSERT INTO genres (
        genre_name, 
        genre_description, 
        origin_year, 
        ranking, 
        country_of_genre
    )
    VALUES (
        p_genre_name, 
        p_genre_description, 
        p_origin_year, 
        p_ranking, 
        p_country_of_genre
    );
END$$

DELIMITER ;






-- Task2 b ----------------------------------------------------------------------------------------------------------------

CREATE TABLE user_playlists (
    user_id INT NOT NULL,
    playlist_id INT NOT NULL,
    PRIMARY KEY (user_id, playlist_id),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(user_id),
    CONSTRAINT fk_playlist FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id)
);

DELIMITER $$
DROP PROCEDURE IF EXISTS link_user_to_playlist;
CREATE PROCEDURE link_user_to_playlist(
    IN p_username VARCHAR(50),
    IN p_playlist_name VARCHAR(100)
)
BEGIN
    DECLARE v_user_id INT;
    DECLARE v_playlist_id INT;

    -- Отримати user_id за username
    SELECT user_id INTO v_user_id
    FROM users
    WHERE username = p_username;

    -- Якщо користувач не знайдений, згенерувати помилку
    IF v_user_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'User not found';
    END IF;

    -- Отримати playlist_id за playlist_name
    SELECT playlist_id INTO v_playlist_id
    FROM playlists
    WHERE playlist_name = p_playlist_name;

    -- Якщо плейлист не знайдений, згенерувати помилку
    IF v_playlist_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Playlist not found';
    END IF;

    -- Вставити запис у стикувальну таблицю
    INSERT INTO user_playlists (user_id, playlist_id)
    VALUES (v_user_id, v_playlist_id);
END$$

DELIMITER ;

-- Task 2 c -----------------------------------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS insert_noname_genres;

DELIMITER $$

CREATE PROCEDURE insert_noname_genres()
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE base_origin_year INT DEFAULT 2000;
    DECLARE base_ranking INT DEFAULT 10;

    -- Цикл для вставки 10 записів
    WHILE i <= 10 DO
        INSERT INTO genres (genre_name, genre_description, origin_year, ranking, country_of_genre)
        VALUES (
            CONCAT('Noname', i),                        -- genre_name
            CONCAT('Description for Noname', i),       -- genre_description
            base_origin_year + i,                      -- origin_year
            base_ranking + i,                          -- ranking
            'Unknown'                                  -- country_of_genre
        );
        SET i = i + 1;  -- Збільшення лічильника
    END WHILE;
END$$

DELIMITER ;

-- Task 2 d ----------------------------------------------------------------------------------------------------------------------------

DELIMITER $$

CREATE FUNCTION calculate_total_tracks_stats(stat_type VARCHAR(10))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE result DECIMAL(10,2);

    -- Обчислення на основі параметра stat_type
    IF stat_type = 'MAX' THEN
        SELECT MAX(total_tracks) INTO result FROM albums;
    ELSEIF stat_type = 'MIN' THEN
        SELECT MIN(total_tracks) INTO result FROM albums;
    ELSEIF stat_type = 'SUM' THEN
        SELECT SUM(total_tracks) INTO result FROM albums;
    ELSEIF stat_type = 'AVG' THEN
        SELECT AVG(total_tracks) INTO result FROM albums;
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid stat_type. Use MAX, MIN, SUM, or AVG.';
    END IF;

    RETURN result;
END$$

DELIMITER ;


SELECT calculate_total_tracks_stats('MAX'); 
SELECT calculate_total_tracks_stats('MIN'); 
SELECT calculate_total_tracks_stats('SUM'); 
SELECT calculate_total_tracks_stats('AVG'); 

SELECT calculate_total_tracks_stats('MAX') AS result;


-- Task 2 e i ---------------------------------------------------------------------------------------------------------------------------------------



DROP PROCEDURE IF EXISTS split_users_randomly;

DELIMITER $$

CREATE PROCEDURE split_users_randomly()
BEGIN
    -- Змінні для даних з таблиці users
    DECLARE v_username VARCHAR(50);
    DECLARE v_email VARCHAR(100);
    DECLARE v_password VARCHAR(100);
    DECLARE v_gender VARCHAR(1);
    DECLARE v_birthdayDate DATE;
    
    -- Прапорець завершення
    DECLARE done INT DEFAULT 0;
    
    -- Курсор для вибору даних з таблиці users
    DECLARE user_cursor CURSOR FOR
        SELECT username, email, password, gender, birthdayDate
        FROM users;
    
    -- Обробка завершення курсора
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    -- Створення таблиць user_part1 та user_part2
    CREATE TABLE IF NOT EXISTS user_part1 (
        new_user_id INT AUTO_INCREMENT PRIMARY KEY, -- Новий PRIMARY KEY
        username VARCHAR(50),
        email VARCHAR(100),
        password VARCHAR(100),
        gender VARCHAR(1),
        birthdayDate DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS user_part2 (
        new_user_id INT AUTO_INCREMENT PRIMARY KEY, -- Новий PRIMARY KEY
        username VARCHAR(50),
        email VARCHAR(100),
        password VARCHAR(100),
        gender VARCHAR(1),
        birthdayDate DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Відкрити курсор
    OPEN user_cursor;

    -- Цикл обробки даних курсора
    read_loop: LOOP
        FETCH user_cursor INTO v_username, v_email, v_password, v_gender, v_birthdayDate;
        
        -- Перевірка завершення вибірки
        IF done = 1 THEN
            LEAVE read_loop;
        END IF;
        
        -- Випадкове визначення таблиці для вставки
        IF RAND() < 0.5 THEN
            -- Вставка в user_part1
            INSERT INTO user_part1 (username, email, password, gender, birthdayDate)
            VALUES (v_username, v_email, v_password, v_gender, v_birthdayDate);
        ELSE
            -- Вставка в user_part2
            INSERT INTO user_part2 (username, email, password, gender, birthdayDate)
            VALUES (v_username, v_email, v_password, v_gender, v_birthdayDate);
        END IF;
    END LOOP;

    -- Закрити курсор
    CLOSE user_cursor;

    -- Повернути імена таблиць
    SELECT 'user_part1' AS table1, 'user_part2' AS table2;
END$$

DELIMITER ;


CALL split_users_randomly();

SELECT * FROM user_part1;
SELECT * FROM user_part2;



-- Task 3 a ---------------------------------------------------------------------------------------------------------------------------------
-- Видалення тригера, якщо вже існує
DROP TRIGGER IF EXISTS before_insert_genres;
DROP TRIGGER IF EXISTS before_update_genres;

DELIMITER $$

-- Тригер перед вставкою
CREATE TRIGGER before_insert_genres
BEFORE INSERT ON genres
FOR EACH ROW
BEGIN
    -- Перевірка, чи закінчується значення ranking двома нулями
    IF NEW.ranking % 100 = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'The ranking value cannot end with two zeros.';
    END IF;
END$$

-- Тригер перед оновленням
CREATE TRIGGER before_update_genres
BEFORE UPDATE ON genres
FOR EACH ROW
BEGIN
    -- Перевірка, чи закінчується значення ranking двома нулями
    IF NEW.ranking % 100 = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'The ranking value cannot end with two zeros.';
    END IF;
END$$

DELIMITER ;




-- Task 3 f -- -------------------------------------------------------------------------------------------------------------------------------------
-- Створення таблиці журналу для запису видалених даних
CREATE TABLE IF NOT EXISTS genres_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,         -- Унікальний ідентифікатор запису
    genre_id INT NOT NULL,                         -- ID видаленого жанру
    genre_name VARCHAR(50) NOT NULL,               -- Назва жанру
    genre_description VARCHAR(255) NOT NULL,      -- Опис жанру
    origin_year YEAR,                              -- Рік виникнення
    ranking INT,                                   -- Рейтинг жанру
    country_of_genre VARCHAR(50),                 -- Країна жанру
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Час видалення
);

-- Видалення існуючого тригера, якщо він є
DROP TRIGGER IF EXISTS log_genre_deletion;

DELIMITER $$

-- Створення тригера для запису видалення жанру
CREATE TRIGGER log_genre_deletion
AFTER DELETE ON genres
FOR EACH ROW
BEGIN
    -- Вставка запису у таблицю журналу при видаленні з genres
    INSERT INTO genres_log (genre_id, genre_name, genre_description, origin_year, ranking, country_of_genre)
    VALUES (OLD.genre_id, OLD.genre_name, OLD.genre_description, OLD.origin_year, OLD.ranking, OLD.country_of_genre);
END$$

DELIMITER ;

DELETE FROM genres WHERE genre_id = 44;




-- Task 3 j -----------------------------------------------------------------------------------------------------------------------------
-- Видаляємо тригер, якщо він уже існує
DROP TRIGGER IF EXISTS before_insert_or_update_users;

DELIMITER $$

-- Створюємо тригер для перевірки username
CREATE TRIGGER before_insert_or_update_users
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    -- Перевіряємо, чи username є одним із дозволених значень
    IF NEW.username NOT IN ('svitlana', 'petro', 'olha', 'taras') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid username. Allowed values are: svitlana, petro, olha, taras.';
    END IF;
END$$

DELIMITER $$

-- Створюємо ще один тригер для перевірки під час оновлення
CREATE TRIGGER before_update_users
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    -- Перевіряємо, чи username є одним із дозволених значень
    IF NEW.username NOT IN ('svitlana', 'petro', 'olha', 'taras') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid username. Allowed values are: svitlana, petro, olha, taras.';
    END IF;
END$$

DELIMITER ;


INSERT INTO users (username, email, password, gender, birthdayDate)
VALUES ('svitlana', 'svitlana@example.com', 'password123', 'F', '1990-01-01');





