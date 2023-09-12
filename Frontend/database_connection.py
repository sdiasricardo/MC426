import sqlalchemy as sa
class DatabaseConnection:
    def __init__(self, db_url):
        self.engine = sa.create_engine(db_url)
        metadata = sa.Metadata()
        self.users = sa.Table(
            'users',
            metadata,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('username', sa.String(50)),
            sa.Column('email', sa.String(100)),
            sa.Column('password', sa.String(100))
        )
        metadata.create_all(self.engine)

    def user_exists(self, name, email):

        query = sa.select([self.users]).where(
            (self.users.c.username == name) | (self.users.c.email == email)
        )

        connection = self.engine.connect()

        result = connection.execute(query)

        connection.close()

        return not result.fetchone()

    def create_user(self, user):

        insert = sa.insert(self.users).values(username=user.Name, email=user.Email, password=user.Password)

        connection = self.engine.connect()

        try:
            connection.execute(insert)

        except Exception as e:
            print(f"Error inserting user: {e}")

        connection.close()
