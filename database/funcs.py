from sqlalchemy.orm import Session
from sqlalchemy.sql.ddl import DropSchema, CreateSchema
from database.connection import engine
from database.models import SCHEMA_NAME, Base, User
from sqlalchemy.exc import IntegrityError


def recreate_database():
    with engine.connect() as connection:
        connection.execute(DropSchema(SCHEMA_NAME, cascade=True, if_exists=True))
        connection.execute(CreateSchema(SCHEMA_NAME, if_not_exists=True))
        connection.commit()
    Base.metadata.create_all(engine)
    print("База успешно пересоздана")


def create_database():
    with engine.connect() as connection:
        connection.execute(CreateSchema(SCHEMA_NAME, if_not_exists=True))
        connection.commit()
    Base.metadata.create_all(engine)
    print("База успешно создана")


def get_user_by_login(login):
    with Session(engine) as session:
        result = session.query(User).filter(User.login == login).first()
    return result


def create_user(login, password):
    user = User(login=login, password=password)
    try:
        with Session(engine) as session:
            session.add(user)
            session.commit()
    except IntegrityError:
        return None
    return user

