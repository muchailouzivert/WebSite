import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from main.models import User, Base
from main.repositories.User import UserRepository


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.Session = Session(bind=self.engine)
        Base.metadata.create_all(self.engine)

        self.session = self.Session

        new_user1 = User(username='test_user1', password='test_password1')
        new_user2 = User(username='test_user2', password='test_password2')
        self.session.add(new_user1)
        self.session.add(new_user2)
        self.session.commit()

        self.user_repository = UserRepository(db_session=self.session)

    def tearDown(self):
        self.session.close()

    def test_create_user(self):
        test_username = 'test_user'
        test_password = 'test_password'

        new_user = self.user_repository.create_user(username=test_username, password=test_password)

        retrieved_user = self.session.query(User).filter_by(username=test_username).first()

        # Assert that add and refresh methods were called
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, new_user.username)
        self.assertEqual(retrieved_user.password, new_user.password)

    def test_get_user_by_id(self):
        # Mock the get method
        user = self.user_repository.get_user_by_id(user_id=1)

        # Assert that get method was called
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, "test_user1")
        self.assertEqual(user.password, "test_password1")

    def test_get_user_by_username(self):
        # Mock the execute and scalars methods
        user = self.user_repository.get_user_by_username(username="test_user2")

        # Assert that execute and scalars methods were called
        self.assertEqual(user.id, 2)
        self.assertEqual(user.username, "test_user2")
        self.assertEqual(user.password, "test_password2")

    def test_get_all_users(self):
        # Mock the query and all methods
        users = self.user_repository.get_all_users()

        # Assert that query and all methods were called
        self.assertEqual(len(users), 2)

    def test_update_user(self):
        # Mock the execute method
        self.user_repository.update_user(user_id=1, new_username="newuser", new_password="newpass")

        user = self.user_repository.get_user_by_id(user_id=1)

        # Assert that execute method was called
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.password, "newpass")

    def test_delete_user(self):
        # Assert that query, get, and delete methods were called
        self.user_repository.delete_user(user_id=1)

        deleted_user = self.session.query(User).get(1)
        self.assertIsNone(deleted_user)


if __name__ == '__main__':
    unittest.main()
