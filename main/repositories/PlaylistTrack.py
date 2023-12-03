from main.models import PlaylistTrack


class PlaylistTrackRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_playlist_track(self, playlist_id, track_id, order):
        try:
            new_playlist_track = PlaylistTrack(playlist_id=playlist_id, track_id=track_id, order=order)
            self.db_session.add(new_playlist_track)
            self.db_session.commit()
            self.db_session.refresh(new_playlist_track)
            return new_playlist_track
        except Exception as e:
            # Handle specific exceptions or log the error
            print(f"Error creating playlist track: {e}")
            self.db_session.rollback()
            return None

    def get_playlist_track(self, playlist_id, track_id):
        try:
            playlist_track = self.db_session.query(PlaylistTrack).get((playlist_id, track_id))
            return playlist_track
        except Exception as e:
            # Handle specific exceptions or log the error
            print(f"Error retrieving playlist track: {e}")
            return None

    def get_all_playlist_tracks(self):
        try:
            playlist_tracks = self.db_session.query(PlaylistTrack).all()
            return playlist_tracks
        except Exception as e:
            # Handle specific exceptions or log the error
            print(f"Error retrieving all playlist tracks: {e}")
            return []

    def update_playlist_track_order(self, playlist_id, track_id, new_order):
        try:
            playlist_track = self.db_session.query(PlaylistTrack).get((playlist_id, track_id))
            if playlist_track:
                playlist_track.order = new_order
                self.db_session.commit()
        except Exception as e:
            # Handle specific exceptions or log the error
            print(f"Error updating playlist track order: {e}")
            self.db_session.rollback()

    def delete_playlist_track(self, playlist_id, track_id):
        try:
            playlist_track = self.db_session.query(PlaylistTrack).get((playlist_id, track_id))
            if playlist_track:
                self.db_session.delete(playlist_track)
                self.db_session.commit()
        except Exception as e:
            # Handle specific exceptions or log the error
            print(f"Error deleting playlist track: {e}")
            self.db_session.rollback()
