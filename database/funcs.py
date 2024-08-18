from sqlalchemy.sql.ddl import DropSchema, CreateSchema
from database.connection import engine
from database.models import SCHEMA_NAME, Base


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
    c