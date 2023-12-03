import unittest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from main.repositories.Track import TrackRepository

# Import the Track, TrackRepository, and other necessary classes here


class TestTrackRepository(unittest.TestCase):
    def setUp(self):
        self.mock_session = Mock(spec=Session)
        self.track_repository = TrackRepository(db_session=self.mock_session)

    def test_create_track(self):
        # Arrange
        track_data = {'title': 'Test Track', 'artist': 'Test Artist', 'duration': 180}

        # Act
        with patch.object(self.mock_session, 'commit') as mock_commit:
            created_track = self.track_repository.create_track(**track_data)

        # Assert
        self.assertIsNotNone(created_track)
        self.assertEqual(created_track.title, 'Test Track')
        self.assertEqual(created_track.artist, 'Test Artist')
        self.assertEqual(created_track.duration, 180)
        mock_commit.assert_called_once()

    def test_get_track(self):
        # Arrange
        track_id = 1
        mock_track = Mock(id=track_id, title='Test Track', artist='Test Artist', duration=180)
        self.mock_session.query.return_value.get.return_value = mock_track

        # Act
        retrieved_track = self.track_repository.get_track(track_id=track_id)

        # Assert
        self.assertIsNotNone(retrieved_track)
        self.assertEqual(retrieved_track.id, track_id)
        self.assertEqual(retrieved_track.title, 'Test Track')
        self.assertEqual(retrieved_track.artist, 'Test Artist')

    def test_get_all_tracks(self):
        # Arrange
        mock_tracks = [
            Mock(id=1, title='Track 1', artist='Artist 1', duration=180),
            Mock(id=2, title='Track 2', artist='Artist 2', duration=200),
        ]
        self.mock_session.query.return_value.all.return_value = mock_tracks

        # Act
        all_tracks = self.track_repository.get_all_tracks()

        # Assert
        self.assertEqual(len(all_tracks), 2)
        self.assertEqual(all_tracks[0].title, 'Track 1')
        self.assertEqual(all_tracks[1].title, 'Track 2')

    def test_update_track(self):
        # Arrange
        track_id = 1
        updated_data = {'title': 'Updated Track', 'artist': 'Updated Artist', 'duration': 240}
        mock_track = Mock(id=track_id, title='Test Track', artist='Test Artist', duration=180)
        self.mock_session.query.return_value.get.return_value = mock_track

        # Act
        with patch.object(self.mock_session, 'commit') as mock_commit:
            self.track_repository.update_track(track_id=track_id, **updated_data)

        # Assert
        self.assertEqual(mock_track.title, 'Updated Track')
        self.assertEqual(mock_track.artist, 'Updated Artist')
        self.assertEqual(mock_track.duration, 240)
        mock_commit.assert_called_once()

    def test_delete_track(self):
        # Arrange
        track_id = 1
        mock_track = Mock(id=track_id, title='Test Track', artist='Test Artist', duration=180)
        self.mock_session.query.return_value.get.return_value = mock_track

        # Act
        with patch.object(self.mock_session, 'commit') as mock_commit:
            self.track_repository.delete_track(track_id=track_id)

        # Assert
        mock_commit.assert_called_once()
        self.mock_session.query.return_value.get.assert_called_once_with(track_id)


if __name__ == '__main__':
    unittest.main()
