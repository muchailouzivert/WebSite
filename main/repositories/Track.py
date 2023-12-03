from sqlalchemy.orm import exc

from main.models import Track


class TrackRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_track(self, title, artist, duration):
        try:
            new_track = Track(title=title, artist=artist, duration=duration)
            self.db_session.add(new_track)
            self.db_session.commit()
            self.db_session.refresh(new_track)
            return new_track
        except Exception as e:
            # Handle specific exceptions or log the error
            print(f"Error creating track: {e}")
            self.db_session.rollback()
            return None

    def get_track(self, track_id):
        try:
            track = self.db_session.query(Track).get(track_id)
            return track
        except exc.NoResultFound:
            # Handle the case where the track is not found
            print(f"Track with ID {track_id} not found.")
            return None
        except Exception as e:
            # Handle other exceptions or log the error
            print(f"Error retrieving track: {e}")
            return None

    def get_all_tracks(self):
        try:
            tracks = self.db_session.query(Track).all()
            return tracks
        except Exception as e:
            # Handle specific exceptions or log the error
            print(f"Error retrieving all tracks: {e}")
            return []

    def update_track(self, track_id, title=None, artist=None, duration=None):
        try:
            track = self.db_session.query(Track).get(track_id)
            if track:
                if title is not None:
                    track.title = title
                if artist is not None:
                    track.artist = artist
                if duration is not None:
                    track.duration = duration

                self.db_session.commit()
        except Exception as e:
            # Handle specific exceptions or log the error
            print(f"Error updating track: {e}")
            self.db_session.rollback()

    def delete_track(self, track_id):
        try:
            track = self.db_session.query(Track).get(track_id)
            if track:
                self.db_session.delete(track)
                self.db_session.commit()
        except Exception as e:
            # Handle specific exceptions or log the error
            print(f"Error deleting track: {e}")
            self.db_session.rollback()
