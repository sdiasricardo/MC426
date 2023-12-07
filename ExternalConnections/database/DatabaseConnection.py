import sqlalchemy as sa
import logging
import sys
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
absolute_directory = os.path.dirname(parent_directory)
sys.path.append(absolute_directory) 

from Entities.Enums.UserSituation import UserSituation
from Entities.User import User


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
            sa.Column('receive_notifications', sa.Boolean(100))
        )
        self.metadata.create_all(self.engine)

        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    def user_exists(self, name, email):
        query = sa.select(self.users).where(
            sa.or_(self.users.c.username == name, self.users.c.email == email)
        )

        connection = self.engine.connect()

        result = connection.execute(query)

        possible_user = result.fetchone()

        connection.close()

        if possible_user is not None:
            if possible_user.email == email:
                return UserSituation.EMAIL_TAKEN

            return UserSituation.USERNAME_TAKEN

        return UserSituation.SUCCESS

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

    def get_all_users(self):
        query = sa.select(self.users)

        connection = self.engine.connect()

        result = connection.execute(query)

        users = result.fetchall()

        connection.close()

        return users




