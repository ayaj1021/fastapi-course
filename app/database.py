from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Database url format
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
#SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
SQLALCHEMY_DATABASE_URL = "postgresql://postgressql_fastapi_course_user:uMluego05GoOdXV8QINu0RFLI2sIAOx4@dpg-d3o85ter433s739scfeg-a.oregon-postgres.render.com/postgressql_fastapi_course"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# This is what we do to connect to our database
# To ensure that our database continues running till we get a connection we use a while loop
# Just incase we haven't connected to our database because of a password error or any other error
# But since we are using sqlalchemy, we won't be needing this

# while True:

#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="verifi",
#             user="postgres",
#             password="14hs1021",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful!!!")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: ", error)
#         time.sleep(2)



#Instead of using sqlachemy to interact with our db, we can use alembic.
#Because this allows us to be able to modify our tables in our db
#So we install Alembic, pip install alembic
#Then we initialize it alembic init alembic[This could be any name]