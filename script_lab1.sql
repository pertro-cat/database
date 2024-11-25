-- Створення схеми бази даних
CREATE SCHEMA IF NOT EXISTS music_service_itunes;
USE music_service_itunes1;

-- Таблиця albums
CREATE TABLE albums (
    album_id INT AUTO_INCREMENT PRIMARY KEY,
    album_name VARCHAR(100) NOT NULL,
    release_date DATE,
    label_id INT,
    total_tracks INT,
    duration TIME,
    language VARCHAR(20),
    genre_id INT,
    awards_nomanation TEXT,
    INDEX idx_label_id (label_id),
    INDEX idx_genre_id (genre_id),
    FOREIGN KEY (label_id) REFERENCES labels(label_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

-- Таблиця authors
CREATE TABLE authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    author_name VARCHAR(100) NOT NULL,
    bio TEXT,
    awards TEXT,
    genres VARCHAR(255),
    debut_year YEAR,
    song_id INT,
    INDEX idx_song_id (song_id),
    FOREIGN KEY (song_id) REFERENCES songs(song_id)
);

-- Таблиця genres
CREATE TABLE genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(50) NOT NULL,
    genre_description VARCHAR(255),
    origin_year YEAR,
    ranking INT,
    country_of_genre VARCHAR(50),
    INDEX idx_album_id (album_id),
    INDEX idx_song_id (song_id)
);

-- Таблиця labels
CREATE TABLE labels (
    label_id INT AUTO_INCREMENT PRIMARY KEY,
    label_name VARCHAR(100) NOT NULL,
    founded_year YEAR,
    founder VARCHAR(100),
    artist_count INT,
    INDEX idx_album_id (album_id),
    INDEX idx_song_id (song_id)
);

-- Таблиця library
CREATE TABLE library (
    library_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    playlist_id INT,
    author_id INT,
    creation_date DATE,
    access_count INT,
    last_access_date DATE,
    INDEX idx_user_id (user_id),
    INDEX idx_playlist_id (playlist_id),
    INDEX idx_author_id (author_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id),
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

-- Таблиця playlists
CREATE TABLE playlists (
    playlist_id INT AUTO_INCREMENT PRIMARY KEY,
    playlist_name VARCHAR(100) NOT NULL,
    user_id INT,
    song_id INT,
    description TEXT,
    name_user_who_create VARCHAR(255),
    count_of_song INT,
    total_duration TIME,
    INDEX idx_user_id (user_id),
    INDEX idx_song_id (song_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (song_id) REFERENCES songs(song_id)
);

-- Таблиця songs
CREATE TABLE songs (
    song_id INT AUTO_INCREMENT PRIMARY KEY,
    song_title VARCHAR(100) NOT NULL,
    genre_id INT,
    author_id INT,
    album_id INT,
    label_id INT,
    price DECIMAL(10,2),
    download_count INT,
    duration TIME,
    release_date DATE,
    text_of_song TEXT,
    downloads INT DEFAULT 0,
    INDEX idx_genre_id (genre_id),
    INDEX idx_author_id (author_id),
    INDEX idx_album_id (album_id),
    INDEX idx_label_id (label_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id),
    FOREIGN KEY (author_id) REFERENCES authors(author_id),
    FOREIGN KEY (album_id) REFERENCES albums(album_id),
    FOREIGN KEY (label_id) REFERENCES labels(label_id)
);

-- Таблиця userdownloads
CREATE TABLE userdownloads (
    download_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    song_id INT,
    download_date DATE,
    device_type VARCHAR(50),
    operating_system VARCHAR(50),
    ip_address VARCHAR(45),
    location VARCHAR(100),
    download_method ENUM('Download', 'Stream'),
    INDEX idx_user_id (user_id),
    INDEX idx_song_id (song_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (song_id) REFERENCES songs(song_id)
);

-- Таблиця userfavorite
CREATE TABLE userfavorite (
    favorite_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    author_id INT,
    added_date DATE,
    comment TEXT,
    listen_count INT,
    last_listen_date DATE,
    INDEX idx_user_id (user_id),
    INDEX idx_author_id (author_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

-- Таблиця users
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    gender ENUM('Male', 'Female', 'Other'),
    birthdayDate DATE,
    INDEX idx_download_id (download_id),
    INDEX idx_favorite_id (favorite_id)
);



