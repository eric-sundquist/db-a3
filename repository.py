from mysql.connector import connect, Error


class Repository:
    def __init__(self):
        self.connection = self.init_connection()
        self.cursor = self.connection.cursor()

    def init_connection(self):
        try:
            connection = connect(
                host="localhost",
                database="book_store",
                user="root",
                password="zorro1217",
            )
            return connection
        except Error as error:
            print("Error while connecting to MySQL", error)
            return None

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def store_member(self, val):
        try:
            query = "INSERT INTO Members (fname, lname, adress, city, state, zip, phone, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, val)
            self.connection.commit()
            print("You have registrered successfully!")
        except Error as error:
            # TODO korrekt error om email är dublikerad
            print(error)

    def get_user(self, val):
        try:
            query = "SELECT * FROM Members WHERE email = %s AND password = %s"
            self.cursor.execute(query, val)
            return self.cursor.fetchone()
        except Error:
            return None

    def get_subjects(self):
        try:
            query = "SELECT DISTINCT subject FROM Books ORDER BY subject ASC"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            # TODO korrekt error om email är dublikerad
            print(error)
            return None

    def get_books_by_subject(self, subject):
        print(subject)
        try:
            query = "SELECT * FROM Books WHERE subject = %s"
            self.cursor.execute(query, subject)
            return self.cursor.fetchall()
        except Error as error:
            # TODO korrekt error blabla
            print(error)
            return None
