from psycopg2 import sql

class UserModel:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def add_user(self, username, email, password):
        insert_query = '''
        INSERT INTO users (username, email, password)
        VALUES (%s, %s, %s)
        RETURNING id
        '''
        self.cursor.execute(insert_query, (username, email, password))
        user_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return user_id

    def get_user(self, user_id):
        select_query = '''
        SELECT id, username, email, password
        FROM users
        WHERE id = %s
        '''
        self.cursor.execute(select_query, (user_id,))
        user = self.cursor.fetchone()
        return user

    def update_user(self, user_id, username=None, email=None, password=None):
        update_query = sql.SQL('''
        UPDATE users
        SET {fields}
        WHERE id = %s
        ''').format(fields=sql.SQL(', ').join(
            sql.Composed([sql.Identifier(k), sql.SQL('= %s')]) for k in ['username', 'email', 'password'] if locals()[k] is not None
        ))
        values = [v for v in [username, email, password] if v is not None] + [user_id]
        self.cursor.execute(update_query, values)
        self.connection.commit()

    def delete_user(self, user_id):
        delete_query = '''
        DELETE FROM users
        WHERE id = %s
        '''
        self.cursor.execute(delete_query, (user_id,))
        self.connection.commit()

    def __del__(self):
        self.cursor.close()
        self.connection.close()