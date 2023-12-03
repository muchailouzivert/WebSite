# playlists/models.py
from sqlalchemy import (Column,
                        Integer,
                        String,
                        ForeignKey,
                        Boolean,
                        Text)

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

username = 'root'
password = 'King220lorde'
host = 'localhost'
port = '3306'
database = 'dbplaylistservice'

DATABASE_URL = f"mysql://{username}:{password}@{host}:{port}/{database}"

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    playlists = relationship('Playlist', back_populates='owner')


class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_public = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='playlists')
    tracks = relationship('PlaylistTrack', back_populates='playlist')


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    artist = Column(String(255), nullable=False)
    duration = Column(Integer, nullable=False)

    playlists = relationship('PlaylistTrack', back_populates='track')


class PlaylistTrack(Base):
    __tablename__ = 'playlist_tracks'

    playlist_id = Column(Integer, ForeignKey('playlists.id'), primary_key=True)
    track_id = Column(Integer, ForeignKey('tracks.id'), primary_key=True)
    order = Column(Integer, nullable=False)

    playlist = relationship('Playlist', back_populates='tracks')
    track = relationship('Track', back_populates='playlists')


Engine = create_engine(
    DATABASE_URL, echo=True
)
Base.metadata.create_all(Engine)

Session = sessionmaker(bind=Engine)
