import unittest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from main.repositories.PlaylistTrack import PlaylistTrackRepository


class TestPlaylistTrackRepository(unittest.TestCase):
    def setUp(self):
        # Mock the database session
        self.mock_session = Mock(spec=Session)

        # Create PlaylistTrackRepository instance with the mock session
        self.playlist_track_repository = PlaylistTrackRepository(db_session=self.mock_session)

    def test_create_playlist_track(self):
        # Arrange
        playlist_id, track_id, order = 1, 1, 1

        # Act
        with patch.object(self.mock_session, 'commit') as mock_commit:
            created_playlist_track = self.playlist_track_repository.create_playlist_track(
                playlist_id=playlist_id, track_id=track_id, order=order
            )

        # Assert
        self.assertIsNotNone(created_playlist_track)
        self.assertEqual(created_playlist_track.playlist_id, playlist_id)
        self.assertEqual(created_playlist_track.track_id, track_id)
        self.assertEqual(created_playlist_track.order, order)
        mock_commit.assert_called_once()

    def test_get_playlist_track(self):
        # Arrange
        playlist_id, track_id, order = 1, 1, 1
        mock_playlist_track = Mock(playlist_id=playlist_id, track_id=track_id, order=order)
        self.mock_session.query.return_value.get.return_value = mock_playlist_track

        # Act
        retrieved_playlist_track = self.playlist_track_repository.get_playlist_track(
            playlist_id=playlist_id, track_id=track_id
        )

        # Assert
        self.assertIsNotNone(retrieved_playlist_track)
        self.assertEqual(retrieved_playlist_track.playlist_id, playlist_id)
        self.assertEqual(retrieved_playlist_track.track_id, track_id)
        self.assertEqual(retrieved_playlist_track.order, order)

    def test_get_all_playlist_tracks(self):
        # Arrange
        mock_playlist_tracks = [
            Mock(playlist_id=1, track_id=1, order=1),
            Mock(playlist_id=2, track_id=2, order=2),
        ]
        self.mock_session.query.return_value.all.return_value = mock_playlist_tracks

        # Act
        all_playlist_tracks = self.playlist_track_repository.get_all_playlist_tracks()

        # Assert
        self.assertEqual(len(all_playlist_tracks), 2)
        self.assertEqual(all_playlist_tracks[0].playlist_id, 1)
        self.assertEqual(all_playlist_tracks[1].playlist_id, 2)

    def test_update_playlist_track_order(self):
        # Arrange
        playlist_id, track_id, order = 1, 1, 1
        new_order = 2
        mock_playlist_track = Mock(playlist_id=playlist_id, track_id=track_id, order=order)
        self.mock_session.query.return_value.get.return_value = mock_playlist_track

        # Act
        with patch.object(self.mock_session, 'commit') as mock_commit:
            self.playlist_track_repository.update_playlist_track_order(
                playlist_id=playlist_id, track_id=track_id, new_order=new_order
            )

        # Assert
        self.assertEqual(mock_playlist_track.order, new_order)
        mock_commit.assert_called_once()

    def test_delete_playlist_track(self):
        # Arrange
        playlist_id, track_id, order = 1, 1, 1
        mock_playlist_track = Mock(playlist_id=playlist_id, track_id=track_id, order=order)
        self.mock_session.query.return_value.get.return_value = mock_playlist_track

        # Act
        with patch.object(self.mock_session, 'commit') as mock_commit:
            self.playlist_track_repository.delete_playlist_track(
                playlist_id=playlist_id, track_id=track_id
            )

        # Assert
        mock_commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
