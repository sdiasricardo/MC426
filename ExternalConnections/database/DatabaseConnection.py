import sqlalchemy as sa
import logging
import sys
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
absolute_directory = os.path.dirname(parent_directory)
sys.path.append(absolute_directory) 
sys.path.append(parent_directory + "/Entities/")


from Entities.User import User
from Entities.Enums.UserSignupSituation import UserSignupSituation



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
        self.cities = sa.Table(
            'cities',
            self.metadata,
            sa.Column('user_id', sa.Integer),
            sa.Column('city', sa.String)
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
                return UserSignupSituation.EMAIL_TAKEN

            return UserSignupSituation.USERNAME_TAKEN


        return UserSignupSituation.SUCCESS

    def create_user(self, user):

        insert = sa.insert(self.users).values(username=user.Name, email=user.Email, password=user.Password, receive_notifications= user.ReceiveNotifications)

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
        # query = sa.select(self.users)
        #
        # connection = self.engine.connect()
        #
        # result = connection.execute(query)
        #
        # users = result.fetchall()
        #
        # connection.close()
        #
        # return users
        query = (sa.select(self.users, self.cities))\
            .select_from(self.users.join(self.cities, self.cities.c.user_id == self.users.c.id, isouter=True))

        connection = self.engine.connect()

        result = connection.execute(query)

        users = result.fetchall()

        connection.close()

        max_id = 0
        for user_db in users:
            if user_db[0] > max_id:
                max_id = user_db[0]

        possible_users_list = [None for i in range(0, max_id + 1)]

        for user_db in users:

            if possible_users_list[user_db[0]] is not None:
                possible_users_list[user_db[0]].Cities.append(user_db[7])
                continue

            user = User(user_db[0], user_db[1], user_db[2], user_db[3], receive_notifications=user_db[5])
            user.Cities.append(user_db[7])

            possible_users_list[user_db[0]] = user

        users_list = []
        for possible_user in possible_users_list:
            if possible_user is not None:
                users_list.append(possible_user)

        return users_list



    def validate_user_login(self, username, password):
        query = sa.select(self.users).where(
            sa.and_(self.users.c.username == username, self.users.c.password == password)
        )

        connection = self.engine.connect()


        result = connection.execute(query)

        possible_user = result.fetchone()

        connection.close()

        return possible_user is not None

if __name__ == '__main__':
    db = DatabaseConnection()

    db.get_all_users()