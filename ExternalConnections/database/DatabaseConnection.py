import sqlalchemy as sa
import logging
import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory + "/Entities")
from Enums.user_signup_situation import user_signup_situation


class DatabaseConnection:
    def __init__(self):
        self.engine = sa.create_engine("mysql://root:12345678@localhost/eng_software_teste")
        self.metadata = sa.MetaData()
        self.users = sa.Table(
            'users',
            self.metadata,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('username', sa.String(50)),
            sa.Column('email', sa.String(100)),
            sa.Column('password', sa.String(100)),
            sa.Column('city', sa.String(100)),
            sa.Column('receive_notifications', sa.Boolean(100)),
        )
        self.metadata.create_all(self.engine)

        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    def validate_user_signup(self, name, email):
        query = sa.select(self.users).where(
            sa.or_(self.users.c.username == name, self.users.c.email == email)
        )

        connection = self.engine.connect()

        result = connection.execute(query)

        possible_user = result.fetchone()

        connection.close()

        if possible_user is not None:
            if possible_user.email == email:
                return user_signup_situation.EMAIL_TAKEN

            return user_signup_situation.USERNAME_TAKEN

        return user_signup_situation.SUCCESS

    def create_user(self, user):

        insert = sa.insert(self.users).values(username=user.Name, email=user.Email, password=user.Password)

        connection = self.engine.connect()

        try:
            print("a")
            connection.execute(insert)
            connection.commit()
            print("b")

        except Exception as e:
            print(f"Error inserting user: {e}")

        connection.close()

    def validate_user_login(self, username, password):
        query = sa.select(self.users).where(
            sa.and_(self.users.c.username == username, self.users.c.password == password)
        )

        connection = self.engine.connect()

        result = connection.execute(query)

        possible_user = result.fetchone()

        connection.close()

        return possible_user is not None
