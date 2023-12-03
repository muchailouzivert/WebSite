from typing import Optional, Type

from sqlalchemy.orm import Session
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError

from main.models import User


class UserRepository:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def create_user(self, username: str, password: str) -> User:
        try:
            new_user = User(username=username, password=password)
            with self.db_session.begin():
                self.db_session.add(new_user)
                self.db_session.commit()
        except SQLAlchemyError as e:
            print(f"Error creating user: {e}")
            raise
        return new_user

    def get_user_by_id(self, user_id: int) -> Optional[Type[User]]:
        try:
            return self.db_session.get(User, user_id)
        except SQLAlchemyError as e:
            print(f"Error retrieving user by ID: {e}")
            raise

    def get_user_by_username(self, username: str) -> User:
        try:
            return self.db_session.execute(select(User).filter(User.username == username)).scalars().first()
        except SQLAlchemyError as e:
            print(f"Error retrieving user by username: {e}")
            raise

    def get_all_users(self):
        try:
            return self.db_session.query(User).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving all users: {e}")
            raise

    def update_user(self, user_id: int, new_username: str, new_password: str) -> None:
        try:
            with self.db_session.begin():
                self.db_session.execute(
                    update(User)
                    .where(User.id == user_id)
                    .values(username=new_username, password=new_password)
                )
        except SQLAlchemyError as e:
            print(f"Error updating user: {e}")
            raise
        return

    def delete_user(self, user_id: int) -> None:
        user_delete = self.db_session.query(User).get(user_id)
        self.db_session.commit()
        if user_delete:
            try:
                with self.db_session.begin():
                    self.db_session.delete(user_delete)
                    self.db_session.commit()
            except SQLAlchemyError as e:
                print(f"Error deleting user: {e}")
                raise
        return
