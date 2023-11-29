from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Ad(Base):
    __tablename__ = 'ads'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(String)
    posted_by_id = Column(Integer, ForeignKey('users.id'))
    posted_by = relationship('User', back_populates='ads')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    ads = relationship('Ad', back_populates='posted_by')


engine = create_engine('mysql+mysqlconnector://root:King220lorde@localhost:3306/my_db')

print(User.__table__.create(bind=engine, checkfirst=True))
print(Ad.__table__.create(bind=engine, checkfirst=True))
print("Tables created successfully!")