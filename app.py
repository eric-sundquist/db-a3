from getpass import getpass


class App:
    def __init__(self, repo):
        self.repo = repo

    def run(self):
        # self.main_menu()
        self.user_menu("kalle")

    def main_menu(self):
        """
        Displays the main menu and prompts the user to select an option.
        """
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
        books = []
        while True:
            print("\nMember Menu!")
            print("1. Browse by Subject")
            print("2. Search by Author/Title")
            print("3. Checkout")
            print("4. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                isbn = self.browse_by_subject()
                if isbn is not None:
                    books.append(isbn)
                    print(books)
            elif choice == "2":
                print("Search by author/title")
            elif choice == "3":
                print("Checkout")
            elif choice == "4":
                print("You have been logged out!")
                break
            else:
                print("Invalid choice. Please try again.")

    def browse_by_subject(self):
        subjects = self.repo.get_subjects()
        if subjects is None:
            raise RuntimeError("There was an Error getting the subjects")
        if len(subjects) == 0:
            print("There are no book subjects")

        subject = self.prompt_subject(subjects)
        return self.promt_book(subject)  # return isbn number as string

    def promt_book(self, subject):
        books = self.repo.get_books_by_subject(subject)
        if books is None:
            raise RuntimeError("There was an Error getting the books")
        if len(books) == 0:
            print("There are no books on this subject")
            return None
        print("\nChoose book:")
        print(str(len(books)) + " books available on this subject")
        isbn = None
        for i, book in enumerate(books, start=1):
            self.print_book(book)
            # if i % 2 == 0 or i == len(books):
            #     choice = input(
            #         "\nEnter ISBN to add to Cart or \nn Enter to browse or \nEnter to go back to menu: "
            #     )
            #     if choice == "":
            #         break
            #     if choice == "n":
            #         continue
            #     if self.is_choice_valid_isbn(choice, books):
            #         isbn = choice
            #     else:
            #         print("Invalid choice. Please try again.")
        return isbn

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

        index = input("Enter index of subject: ")
        print()
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
