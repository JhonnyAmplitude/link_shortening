import sqlalchemy
import os


CONNECTION = os.getenv("DB_CONNECTION")


engine = sqlalchemy.create_engine(CONNECTION, echo=False)


with engine.connect() as conn:
    pass
