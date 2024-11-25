from extensions import db

# Модель User для операцій з акаунтом
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum('M', 'F', 'Other'))
    birthdayDate = db.Column(db.Date)

    def to_dict(self):
        """Convert User object to dictionary for JSON representation."""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'gender': self.gender,
            'birthdayDate': self.birthdayDate.strftime('%Y-%m-%d') if self.birthdayDate else None
        }


# Модель Genre для операцій з жанрами
class Genre(db.Model):
    __tablename__ = 'genres'
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(100), nullable=False)
    genre_description = db.Column(db.String(255))
    origin_year = db.Column(db.Integer)
    ranking = db.Column(db.Integer)
    country_of_genre = db.Column(db.String(100))

    # Relationship
    songs = db.relationship('Song', back_populates='genre')

    def to_dict(self):
        """Convert Genre object to dictionary."""
        return {
            'genre_id': self.genre_id,
            'genre_name': self.genre_name,
            'genre_description': self.genre_description,
            'origin_year': self.origin_year,
            'ranking': self.ranking,
            'country_of_genre': self.country_of_genre
        }


# Модель Author для операцій з авторами
class Author(db.Model):
    __tablename__ = 'authors'
    author_id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    awards = db.Column(db.Text)
    debut_year = db.Column(db.Integer)

    # Relationship
    songs = db.relationship('Song', back_populates='author')

    def to_dict(self):
        """Convert Author object to dictionary."""
        return {
            'author_id': self.author_id,
            'author_name': self.author_name,
            'bio': self.bio,
            'awards': self.awards,
            'debut_year': self.debut_year
        }


# Модель Album для операцій з альбомами
class Album(db.Model):
    __tablename__ = 'albums'
    album_id = db.Column(db.Integer, primary_key=True)
    album_name = db.Column(db.String(100), nullable=False)
    realease_date = db.Column(db.Date)
    total_tracks = db.Column(db.Integer)

    # Relationship
    songs = db.relationship('Song', back_populates='album')

    def to_dict(self):
        """Convert Album object to dictionary."""
        return {
            'album_id': self.album_id,
            'album_name': self.album_name,
            'realease_date': self.realease_date.strftime('%Y-%m-%d') if self.realease_date else None,
            'total_tracks': self.total_tracks
        }


# Модель Label для операцій з лейблами
class Label(db.Model):
    __tablename__ = 'labels'
    label_id = db.Column(db.Integer, primary_key=True)
    label_name = db.Column(db.String(100), nullable=False)
    founded_year = db.Column(db.Integer)
    founder = db.Column(db.String(100))

    # Relationship
    songs = db.relationship('Song', back_populates='label')

    def to_dict(self):
        """Convert Label object to dictionary."""
        return {
            'label_id': self.label_id,
            'label_name': self.label_name,
            'founded_year': self.founded_year,
            'founder': self.founder
        }


# Модель Song для операцій з піснями
class Song(db.Model):
    __tablename__ = 'songs'
    
    song_id = db.Column(db.Integer, primary_key=True)
    song_title = db.Column(db.String(100), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.album_id'))
    label_id = db.Column(db.Integer, db.ForeignKey('labels.label_id'))
    price = db.Column(db.Integer)
    download_count = db.Column(db.Integer)
    duraction = db.Column(db.Time)
    realease_date = db.Column(db.Date)
    text_of_song = db.Column(db.Text)
    downloads = db.Column(db.Integer)
    
    # Relationships
    genre = db.relationship('Genre', back_populates='songs')
    author = db.relationship('Author', back_populates='songs')
    album = db.relationship('Album', back_populates='songs')
    label = db.relationship('Label', back_populates='songs')
    downloads = db.relationship(
        'UserDownload',
        secondary='userdownloads_has_songs',
        back_populates='songs'
    )

    def to_dict(self):
        """Convert Song object to dictionary."""
        return {
            'song_id': self.song_id,
            'song_title': self.song_title,
            'genre_id': self.genre_id,
            'author_id': self.author_id,
            'album_id': self.album_id,
            'label_id': self.label_id,
            'price': self.price,
            'download_count': self.download_count,
            'duraction': str(self.duraction),
            'realease_date': str(self.realease_date),
            'text_of_song': self.text_of_song,
            'downloads': self.downloads
        }


# Модель Playlist для операцій з плейлистами
class Playlist(db.Model):
    __tablename__ = 'playlists'
    
    playlist_id = db.Column(db.Integer, primary_key=True)
    playlist_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'), nullable=False)
    description = db.Column(db.String(255))
    name_user_who_create = db.Column(db.String(50))
    count_of_song = db.Column(db.Integer)
    total_duraction = db.Column(db.Time)

    # Relationships
    user = db.relationship('User', backref='playlists')
    song = db.relationship('Song', backref='playlists')

    def to_dict(self):
        """Convert Playlist object to dictionary."""
        return {
            'playlist_id': self.playlist_id,
            'playlist_name': self.playlist_name,
            'user_id': self.user_id,
            'song_id': self.song_id,
            'description': self.description,
            'name_user_who_create': self.name_user_who_create,
            'count_of_song': self.count_of_song,
            'total_duraction': str(self.total_duraction) if self.total_duraction else None
        }


# Модель UserFavoriteArtist для улюблених артистів користувача
class UserFavoriteArtist(db.Model):
    __tablename__ = 'userfavoriteartists'

    favorite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'), nullable=False)
    added_date = db.Column(db.Date)
    comment = db.Column(db.Text)
    listen_count = db.Column(db.Integer)
    last_listen_date = db.Column(db.Date)

    # Визначення зв'язків з таблицями users та authors
    user = db.relationship('User', backref=db.backref('favorite_artists', cascade="all, delete-orphan"))
    author = db.relationship('Author', backref=db.backref('fans', cascade="all, delete-orphan"))

    def to_dict(self):
        """Convert UserFavoriteArtist object to dictionary for JSON serialization."""
        return {
            'favorite_id': self.favorite_id,
            'user_id': self.user_id,
            'author_id': self.author_id,
            'added_date': str(self.added_date) if self.added_date else None,
            'comment': self.comment,
            'listen_count': self.listen_count,
            'last_listen_date': str(self.last_listen_date) if self.last_listen_date else None
        }


# Стикувальна таблиця для зв'язку "багато до багатьох" між UserDownload та Song
class UserDownloadHasSong(db.Model):
    __tablename__ = 'userdownloads_has_songs'
    
    userdownloads_download_id = db.Column(
        db.Integer,
        db.ForeignKey('userdownloads.download_id', ondelete="CASCADE"), 
        primary_key=True
    )
    songs_song_id = db.Column(
        db.Integer,
        db.ForeignKey('songs.song_id', ondelete="CASCADE"), 
        primary_key=True
    )

    def to_dict(self):
        """Convert UserDownloadHasSong object to dictionary."""
        return {
            'userdownloads_download_id': self.userdownloads_download_id,
            'songs_song_id': self.songs_song_id
        }


# Модель UserDownload для операцій з завантаженнями
class UserDownload(db.Model):
    __tablename__ = 'userdownloads'
    
    download_id = db.Column(db.Integer, primary_key=True)
    release_date = db.Column(db.Date)  # Corrected the typo here
    # Інші колонки для моделі UserDownload...
    
    # Зв'язок багато до багатьох з Song через UserDownloadHasSong
    songs = db.relationship(
        'Song',
        secondary='userdownloads_has_songs',
        back_populates='downloads'
    )

    def to_dict(self):
        """Convert UserDownload object to dictionary."""
        return {
            'download_id': self.download_id,
            'release_date': self.release_date,  # Corrected the typo here
            'songs': [song.to_dict() for song in self.songs]
        }

