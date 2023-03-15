from datetime import datetime, timedelta
from getpass import getpass


class App:
    def __init__(self, repo):
        self.repo = repo

    def run(self):
        self.main_menu()

    def main_menu(self):
        while True:
            print("\nWelcome to the Book Store!")
            print("1. Member Login")
            print("2. New Member Registration")
            print("3. Quit")
            choice = input("Enter your choice: ")
            if choice == "1":
                user = self.login()
                if user is not None:
                    self.user_menu(user)
                else:
                    print("Email or password incorrect")
            elif choice == "2":
                self.create_member()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def user_menu(self, user):
        while True:
            isbn = None
            print("\nMember Menu!")
            print("1. Browse by Subject")
            print("2. Search by Author/Title")
            print("3. Checkout")
            print("4. Logout")
            choice = input("Enter your choice: ")
            if choice == "1":
                isbn = self.browse_by_subject()
            elif choice == "2":
                isbn = self.search_author_title()
            elif choice == "3":
                self.cart(user)
            elif choice == "4":
                print("\nYou have been logged out!")
                break
            else:
                print("\nInvalid choice. Please try again.")
            if isbn is not None:
                self.repo.add_to_cart(user[0], isbn, self.prompt_qty())

    def cart(self, user):
        cart = self.repo.get_cart(user[0])
        print("\nCheckout")
        if len(cart) == 0:
            print("\nThe cart is empty!")
            return None
        print("\nCurrent Cart Contents: ")
        self.print_cart(cart)
        while True:
            action = input("\nProceed to check out? (Y/N): ").lower()
            if action == "y":
                self.checkout(user, cart)
                break
            if action == "n":
                break
            print("Invalid input. Try again.")

    def checkout(self, user, cart):
        date = datetime.now().strftime("%Y-%m-%d")
        order_no = self.repo.create_order(user, date)
        for book in cart:
            self.repo.create_order_detail(
                order_no, book[0], book[3], round(book[2] * book[3], 2)
            )
        self.repo.delete_cart(user[0])
        print("\nOrder Details:")
        self.print_order_details(order_no, date, user)
        self.print_cart(cart)

    def print_order_details(self, order_no, date, user):
        print("Invoice for order no." + str(order_no))
        print("\nShipping adress")
        print("Name: " + user[1] + " " + user[2])
        print("Adress: " + user[3])
        print("City: " + user[4])
        print("State: " + user[5])
        print("Zip: " + str(user[6]))
        d1 = datetime.strptime(date, "%Y-%m-%d")
        d2 = d1 + timedelta(days=7)
        print("\n Estimated delivery: " + d2.strftime("%Y-%m-%d"))

    def print_cart(self, cart):
        tot_price = 0
        for book in cart:
            print("\nISBN: " + book[0])
            print("Title: " + book[1])
            print("Price: $" + str(book[2]))
            print("Quantity: " + str(book[3]))
            price = book[2] * book[3]
            tot_price += price
            print("Total price: $" + str(round(price, 2)))
        print("\nTotal price of all books: $" + str(round(tot_price, 2)))

    def search_author_title(self):
        while True:
            print("\n1. Author Search")
            print("2. Title Search")
            print("3. Go back to Member Menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                return self.author_search()
            if choice == "2":
                return self.title_search()
            if choice == "3":
                return None
            print("\nInvalid choice. Please try again.")

    def author_search(self):
        user_input = self.prompt_string_input(
            "Enter name of the Author or part of the name: "
        ).strip()
        books = self.repo.search_by("author", user_input)
        return self.print_books_prompt_isbn(books, 3)

    def title_search(self):
        user_input = self.prompt_string_input(
            "Enter Title or part of the Title: "
        ).strip()
        books = self.repo.search_by("title", user_input)
        return self.print_books_prompt_isbn(books, 3)

    def prompt_string_input(self, prompt):
        while True:
            user_input = input(prompt)
            if len(user_input) <= 255:
                return user_input
            print("Invalid input. Please try again.")

    # Use the user_input variable here

    def browse_by_subject(self):
        subjects = self.repo.get_subjects()
        if subjects is None:
            raise RuntimeError("\nThere was an Error getting the subjects")
        if len(subjects) == 0:
            print("\nThere are no book subjects")
        subject = self.prompt_subject(subjects)
        return self.get_isbn_by_subj(subject)  # return isbn number as string

    def get_isbn_by_subj(self, subject):
        books = self.repo.get_books_by_subject(subject)
        if books is None:
            raise RuntimeError("\nThere was an Error getting the books")
        if len(books) == 0:
            print("\nThere are no books on this subject")
            return None
        return self.print_books_prompt_isbn(books, 2)

    def print_books_prompt_isbn(self, books, nr_books_display):
        amount_books = len(books)
        if amount_books == 0:
            print("\nNo books where found")
        elif amount_books == 1:
            print("\n1 book found.")
        else:
            print("\n" + str(len(books)) + " books found")
        for i, book in enumerate(books, start=1):
            self.print_book(book)
            if i % nr_books_display == 0 or i == len(books):
                while True:
                    choice = input(
                        "\nEnter ISBN to add to Cart or \nn Enter to browse or \nEnter to go back to menu: "
                    )
                    if choice == "":
                        return None
                    if choice == "n":
                        break
                    if self.is_choice_valid_isbn(choice, books):
                        return choice
                    print("\nInvalid choice. Please try again.")
        return None

    def prompt_qty(self):
        while True:
            try:
                value = int(input("Enter quantity: "))
                if 1 <= value:
                    return value
                print("The quantity must be 1 or above.")
            except ValueError:
                print("Invalid input, please enter an integer.")

    def print_book(self, book):
        print("\nAuthor: " + book[1])
        print("Title: " + book[2])
        print("ISBN: " + book[0])
        print("PRICE: " + str(book[3]))
        print("Subject: " + book[4])

    def is_choice_valid_isbn(self, choice, books):
        for book in books:
            isbn = book[0]
            if isbn == choice:
                return True
        return False

    def prompt_subject(self, subjects):
        print("\nChoose subject:")
        for i, subject in enumerate(subjects, start=1):
            print(str(i) + ". " + subject[0])
        index = None
        while True:
            try:
                index = int(input("Enter index of subject: "))
            except ValueError:
                print("Input must be an integer")
                continue
            if 1 <= index <= len(subjects):
                break
            print("Input must be between 1 and " + str(len(subjects)) + "!")
        return subjects[int(index) - 1]

    def create_member(self):
        print("\nNew Member Registration")
        fname = input("Enter first name: ")
        lname = input("Enter last name: ")
        adress = input("Enter street adress: ")
        city = input("Enter city: ")
        state = input("Enter state: ")
        zipnr = input("Enter zip: ")
        phone = input("Enter phone: ")
        # TODO Validera som giltig adress?
        email = input("Enter email: ")
        password = getpass("Enter password: ")

        self.repo.store_member(
            (fname, lname, adress, city, state, zipnr, phone, email, password)
        )

    def login(self):
        print("\nLogin in to your account")
        email = input("Email: ")
        password = getpass("Password: ")
        return self.repo.get_user((email, password))
