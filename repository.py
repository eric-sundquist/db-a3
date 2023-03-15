from mysql.connector import connect, Error, IntegrityError
import bcrypt


class Repository:
    def __init__(self):
        self.connection = self.init_connection()
        self.cursor = self.connection.cursor()

    def init_connection(self):
        try:
            connection = connect(
                host="localhost",  # TODO CONFIG
                database="book_store",
                user="root",
                password="<password>",
            )
            return connection
        except Error as error:
            print("Error while connecting to MySQL", error)
            return None

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def store_member(self, user_data, password):
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        val = user_data + (hashed_password,)
        try:
            query = "INSERT INTO Members (fname, lname, adress, city, state, zip, phone, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, val)
            self.connection.commit()
            print("You have registrered successfully!")
        except IntegrityError:
            print("Email already exists, try another email")
        except Error as error:
            print(f"Error: {error}")

    def get_user(self, email, password):
        try:
            val = (email,)
            query = "SELECT * FROM Members WHERE email = %s"
            self.cursor.execute(query, val)
            user = self.cursor.fetchone()
            if user is not None:
                hashed_password = user[9]
                if bcrypt.checkpw(
                    password.encode("utf-8"), hashed_password.encode("utf-8")
                ):
                    return user
            return None
        except Error as error:
            print(f"Error: {error}")
            return None

    def get_subjects(self):
        try:
            query = "SELECT DISTINCT subject FROM Books ORDER BY subject ASC"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            print(f"Error: {error}")
            return None

    def get_books_by_subject(self, subject):
        query = "SELECT * FROM Books WHERE subject = %s"
        try:
            self.cursor.execute(query, subject)
            return self.cursor.fetchall()
        except Error as error:
            print(f"Error: {error}")
            return None

    def add_to_cart(self, user_id, isbn, qty):
        query = "INSERT INTO Cart (userid, isbn, qty) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE qty = %s"
        val = (user_id, isbn, qty, qty)
        try:
            self.cursor.execute(query, val)
            self.connection.commit()
            return None
        except Error as error:
            print(f"Error: {error}")
            return None

    def get_cart(self, user_id):
        query = "SELECT b.isbn, b.title, b.price, c.qty FROM Cart c JOIN Books b ON c.isbn = b.isbn WHERE c.userid =  %s"
        val = (user_id,)
        try:
            self.cursor.execute(query, val)
            return self.cursor.fetchall()
        except Error as error:
            print(f"Error: {error}")
            return None

    def search_by(self, search_by, sub_str):
        if search_by == "author":
            query = "SELECT * FROM Books WHERE author LIKE %s"
        else:
            query = "SELECT * FROM Books WHERE title LIKE %s"
        val = ("%" + sub_str + "%",)
        try:
            self.cursor.execute(query, val)
            return self.cursor.fetchall()
        except Error as error:
            print(f"Error: {error}")
            return None

    def create_order(self, user, received):
        query = "INSERT INTO Orders (userid, received, shipAdress, shipCity, shipState, shipZip) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (user[0], received, user[3], user[4], user[5], user[6])
        try:
            self.cursor.execute(query, val)
            order_no = self.cursor.lastrowid
            self.connection.commit()
            return order_no
        except Error as error:
            print(f"Error: {error}")
            return None

    def create_order_detail(self, ono, isbn, qty, price):
        query = (
            "INSERT INTO OrderDetails (ono, isbn, qty, price) VALUES (%s, %s, %s, %s)"
        )
        val = (ono, isbn, qty, price)
        try:
            self.cursor.execute(query, val)
            self.connection.commit()
            return None
        except Error as error:
            print(f"Error: {error}")
            return None

    def delete_cart(self, userid):
        query = "DELETE FROM Cart WHERE userid = %s"
        val = (userid,)
        try:
            self.cursor.execute(query, val)
            self.connection.commit()
            return None
        except Error as error:
            print(f"Error: {error}")
            return None
