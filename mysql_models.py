import mysql.connector

conn = mysql.connector.connect(host="localhost",user="root", passwd="usbw",db="test")


class User:
    def __init__(self, username, _id=None):
        self.username = username
        self._id = _id

    def create(self):
        
        query = f"INSERT INTO users (username) VALUES (?)"
        cursor = conn.cursor(prepared=True)
        cursor.execute(query, (self.username,))
        conn.commit()
        self.id = cursor.lastrowid
        cursor.close()



        conn.commit()

        print(cursor.rowcount, "record inserted.")

    def get_all():
        users = []
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        for u in cursor.fetchall():
            users.append(User(u[0]))
        cursor.close()
        
        return users
        
        
        

juhani = User('juhanimysql')
juhani.create()