import unittest
from sqlalchemy import create_engine
from main.models import User, Playlist, Base
from main.repositories.Playlist import PlaylistRepository
from sqlalchemy.orm import Session


class TestPlaylistRepository(unittest.TestCase):
    def setUp(self):
        # Create an SQLite in-memory database and a session
        self.engine = create_engine('sqlite:///:memory:')
        self.Session = Session(bind=self.engine)
        Base.metadata.create_all(self.engine)

        self.session = self.Session

        self.playlist_repository = PlaylistRepository(db_session=self.session)

    def tearDown(self):
        # Clean up resources, close the session, etc.
        self.session.close()

    def test_create_playlist(self):
        # Create a user for testing
        new_user = User(username='test_user', password='test_password')
        self.session.add(new_user)
        self.session.commit()

        # Add a playlist to the playlists table
        new_playlist = self.playlist_repository.create_playlist(
            name='Test Playlist',
            description='This is a test playlist',
            is_public=True,
            owner=new_user
        )

        # Verify that the playlist has been added
        retrieved_playlist = self.session.query(Playlist).get(new_playlist.id)
        self.assertIsNotNone(retrieved_playlist)
        self.assertEqual(retrieved_playlist.name, 'Test Playlist')

    def test_get_playlist(self):
        # Create a user for testing
        new_user = User(username='test_user', password='test_password')
        self.session.add(new_user)
        self.session.commit()

        # Add a playlist to the playlists table
        new_playlist = self.playlist_repository.create_playlist(
            name='Test Playlist',
            description='This is a test playlist',
            is_public=True,
            owner=new_user
        )

        # Get the playlist by ID
        retrieved_playlist = self.playlist_repository.get_playlist(playlist_id=new_playlist.id)

        # Verify that the correct playlist has been retrieved
        self.assertIsNotNone(retrieved_playlist)
        self.assertEqual(retrieved_playlist.id, new_playlist.id)
        self.assertEqual(retrieved_playlist.name, 'Test Playlist')

    def test_get_all_playlists(self):
        # Create a user for testing
        new_user = User(username='test_user', password='test_password')
        self.session.add(new_user)
        self.session.commit()

        # Add multiple playlists to the playlists table
        playlist1 = self.playlist_repository.create_playlist(
            name='Playlist 1',
            description='Description 1',
            is_public=True,
            owner=new_user
        )
        playlist2 = self.playlist_repository.create_playlist(
            name='Playlist 2',
            description='Description 2',
            is_public=False,
            owner=new_user
        )
        playlist3 = self.playlist_repository.create_playlist(
            name='Playlist 3',
            description='Description 3',
            is_public=True,
            owner=new_user
        )

        # Get all playlists
        all_playlists = self.playlist_repository.get_all_playlists()

        # Verify that all playlists have been retrieved
        self.assertEqual(len(all_playlists), 3)
        self.assertEqual(all_playlists[0].name, playlist1.name)
        self.assertEqual(all_playlists[1].name, playlist2.name)
        self.assertEqual(all_playlists[2].name, playlist3.name)

    def test_update_playlist(self):
        # Create a user for testing
        new_user = User(username='test_user', password='test_password')
        self.session.add(new_user)
        self.session.commit()

        # Add a playlist to the playlists table
        new_playlist = self.playlist_repository.create_playlist(
            name='Test Playlist',
            description='This is a test playlist',
            is_public=True,
            owner=new_user
        )

        # Update the playlist
        self.playlist_repository.update_playlist(
            playlist_id=new_playlist.id,
            name='Updated Playlist',
            description='Updated description',
            is_public=False
        )

        # Verify that the playlist has been updated
        updated_playlist = self.playlist_repository.get_playlist(playlist_id=new_playlist.id)
        self.assertIsNotNone(updated_playlist)
        self.assertEqual(updated_playlist.name, 'Updated Playlist')
        self.assertEqual(updated_playlist.description, 'Updated description')
        self.assertFalse(updated_playlist.is_public)

    def test_delete_playlist(self):
        # Create a user for testing
        new_user = User(username='test_user', password='test_password')
        self.session.add(new_user)
        self.session.commit()

        # Add a playlist to the playlists table
        new_playlist = self.playlist_repository.create_playlist(
            name='Test Playlist',
            description='This is a test playlist',
            is_public=True,
            owner=new_user
        )

        # Delete the playlist
        self.playlist_repository.delete_playlist(playlist_id=new_playlist.id)

        # Verify that the playlist has been deleted
        deleted_playlist = self.playlist_repository.get_playlist(playlist_id=new_playlist.id)
        self.assertIsNone(deleted_playlist)


if __name__ == '__main__':
    unittest.main()
