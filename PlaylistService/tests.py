from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from PlaylistService.models import Playlist, Song, Comment


class PlaylistAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.public_playlist = Playlist.objects.create(title='Public Playlist', is_public=True, owner=self.user)
        self.private_playlist = Playlist.objects.create(title='Private Playlist', owner=self.user)

    def test_get_public_playlists(self):
        url = reverse('GetPublicPL')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Public Playlist')

    def test_get_all_user_playlists(self):
        url = reverse('GetByUsersPL', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Private Playlist')


class RegisterUserApi(APITestCase):
    @patch('PlaylistService.serializers.UserRegistrationSerializer')
    def test_create_user_successfully(self, mock_serializer):
        url = reverse('user-registration')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }

        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.save.return_value = User(username='testuser')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.last().username, 'testuser')

        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        url = reverse('login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PlaylistViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.playlist = Playlist.objects.create(title='Test Playlist', owner=self.user)

    def test_list_playlists(self):
        url = reverse('playlist-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Playlist')

    def test_retrieve_playlist(self):
        url = reverse('playlist-detail', args=[self.playlist.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Playlist')

    def test_update_playlist(self):
        url = reverse('playlist-detail', args=[self.playlist.id])
        data = {
            "title": "Updated Playlist",
            "description": "string",
            "is_public": 1,
        }
        self.client.force_login(self.user)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Playlist.objects.get(id=self.playlist.id).title, 'Updated Playlist')

    def test_create_playlist(self):
        url = reverse('playlist-list')
        data = {
            "title": "New Playlist",
            "description": "string",
            "is_public": 1,
            "owner": self.user.id
        }
        self.client.force_login(self.user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Playlist.objects.count(), 2)
        self.assertEqual(Playlist.objects.first().title, 'New Playlist')

    def test_delete_playlist(self):
        url = reverse('playlist-detail', args=[self.playlist.id])
        self.client.force_login(self.user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Playlist.objects.count(), 0)


class SongViewSetTest(APITestCase):
    def setUp(self):
        self.song_url = reverse('songs-list')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.playlist = Playlist.objects.create(title='Test Playlist', owner=self.user)
        self.song = Song.objects.create(id=1, title='title', artist="Kame", playlist=self.playlist)

    def test_list_songs(self):
        response = self.client.get(self.song_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_song(self):
        song_id = 1
        song_url = reverse('songs-detail', args=[song_id])
        response = self.client.get(song_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_song(self):
        data = {
            'title': 'New Song',
            'artist': 'New Artist',
            'playlist': self.playlist.id
        }
        response = self.client.post(self.song_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_song(self):
        song_id = 1
        song_url = reverse('songs-detail', args=[song_id])
        data = {
            'title': 'Updated Song Title',
            'artist': 'New Artist'
        }
        response = self.client.put(song_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_song(self):
        song_id = 1
        song_url = reverse('songs-detail', args=[song_id])
        response = self.client.delete(song_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CommentViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.playlist = Playlist.objects.create(title='Test Playlist', owner=self.user)
        self.comment = Comment.objects.create(
            user=self.user,
            text='Test comment',
            playlist=self.playlist
        )

        self.client.force_authenticate(user=self.user)

    def test_list_comments(self):
        url = reverse('comment-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_comment(self):
        url = reverse('comment-detail', kwargs={'pk': self.comment.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'Test comment')

    def test_create_comment(self):
        url = reverse('comment-list')
        data = {
            'user': self.user.id,
            'text': 'New comment',
            'playlist': self.playlist.id,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_update_comment(self):
        url = reverse('comment-detail', kwargs={'pk': self.comment.id})
        data = {'text': 'Updated comment'}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()  # Refresh the object from the database
        self.assertEqual(self.comment.text, 'Updated comment')

    def test_delete_comment(self):
        url = reverse('comment-detail', kwargs={'pk': self.comment.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
