from sqlalchemy.orm import Session
from main.models import Playlist


class PlaylistRepository:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def create_playlist(self, name, description, is_public, owner):
        new_playlist = Playlist(name=name, description=description, is_public=is_public, owner=owner)
        self.db_session.add(new_playlist)
        self.db_session.commit()
        self.db_session.refresh(new_playlist)
        return new_playlist

    def get_playlist(self, playlist_id):
        playlist = self.db_session.query(Playlist).get(playlist_id)
        return playlist

    def get_all_playlists(self):
        playlists = self.db_session.query(Playlist).all()
        return playlists

    def update_playlist(self, playlist_id, name=None, description=None, is_public=None):
        playlist = self.db_session.query(Playlist).get(playlist_id)
        if playlist:
            if name is not None:
                playlist.name = name
            if description is not None:
                playlist.description = description
            if is_public is not None:
                playlist.is_public = is_public

            self.db_session.commit()

    def delete_playlist(self, playlist_id):
        playlist = self.db_session.query(Playlist).get(playlist_id)
        if playlist:
            self.db_session.delete(playlist)
            self.db_session.commit()
