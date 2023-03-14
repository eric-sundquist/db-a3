from getpass import getpass


class App:
    def __init__(self, repo):
        self.repo = repo

    def run(self):
        self.main_menu()
        # self.user_menu("kalle")

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
                print("Checkout")
                cart = self.repo.get_cart(user[0])
                for book in cart:
                    print(book)
            elif choice == "4":
                print("\nYou have been logged out!")
                break
            else:
                print("\nInvalid choice. Please try again.")
            if isbn is not None:
                self.repo.add_to_cart(user[0], isbn, self.prompt_qty())

    def search_author_title(self):
        while True:
            print("1. Author Search")
            print("2. Title Search")
            print("3. Go back to Member Menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                return self.author_search()
            elif choice == "2":
                return self.title_search()
            elif choice == "3":
                break
            else:
                print("\nInvalid choice. Please try again.")

    def author_search(self):
        # TODO
        return "isbn"

    def title_search(self):
        # TODO
        return "isbn"

    def browse_by_subject(self):
        subjects = self.repo.get_subjects()
        if subjects is None:
            raise RuntimeError("\nThere was an Error getting the subjects")
        if len(subjects) == 0:
            print("\nThere are no book subjects")
        subject = self.prompt_subject(subjects)
        return self.promt_book(subject)  # return isbn number as string

    def promt_book(self, subject):
        books = self.repo.get_books_by_subject(subject)
        if books is None:
            raise RuntimeError("\nThere was an Error getting the books")
        if len(books) == 0:
            print("\nThere are no books on this subject")
            return None
        print("\nChoose book:")
        print(str(len(books)) + " books available on this subject")
        isbn = None
        for i, book in enumerate(books, start=1):
            self.print_book(book)
            if i % 2 == 0 or i == len(books):
                exit_loop = False
                while True:
                    choice = input(
                        "\nEnter ISBN to add to Cart or \nn Enter to browse or \nEnter to go back to menu: "
                    )
                    if choice == "":
                        exit_loop = True
                        break
                    if choice == "n":
                        break
                    if self.is_choice_valid_isbn(choice, books):
                        isbn = choice
                        exit_loop = True
                        break

                    print("\nInvalid choice. Please try again.")
                if exit_loop:
                    break
        return isbn

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
        print("\nAuthor: " + book[2])
        print("Title: " + book[1])
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
