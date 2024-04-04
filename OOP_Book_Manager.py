'''
პროგრამა წარმოადგენს წიგნების მენეჯერს. პროგრამის გამოძახების დროს გამოდის მენიუ სადაც მომხმარებელი ირჩევს
წიგნის დამატებას, წიგნის ძებნას ან წიგნების სრული სიის ჩვენებას
პროგრამა მუშაობს მანამ სანამ მომხმარებელი არ მიმართავს Exit ბრძანებს ღილაკით 9

'''
import csv
import os
from datetime import datetime


# წიგნის კლასი ატრიბუტებით: სათაურით, ავტორითა და წიგნის წლით
class Book:
    def __init__(self, book_id, title, author, year):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"'{self.title}' by {self.author} ({self.year})"

# წიგნების მენეჯერ კლასი მეთოდებით 1.წიგნის დამატება 2. წიგნის ძებნა 3. წიგნების სრული სიის გამოტანა
class BookManager:

    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Title", "Author", "Year"])

    def add_book(self, title, author, year):
        new_id = self._get_next_id()
        book = Book(new_id, title, author, year)
        with open(self.filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([book.id, book.title, book.author, book.year])
        print(f"\nBook added: {book}")

    def search_book(self, title):
        found = False
        try:
            with open(self.filename, 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    _, book_title, book_author, book_year = row
                    if title.lower() == book_title.lower():
                        found_book = Book(*row)
                        print(f"\nBook found: {found_book}")
                        found = True
                        break
        except FileNotFoundError:
            print("No books file found.")

        if not found:
            print("\nBook not found, try again!")


    def display_books(self):

        try:
            with open(self.filename, 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader)
                books = list(reader)
                if not books:
                    print("Library is empty, Please add books before displaying")
                    return
                print("\nBooks in library: \n")
                for row in books:
                    print(f"\t{row[0]} - {Book(*row)}")
        except FileNotFoundError:
            print("File does not exist !")

    def _get_next_id(self):
        try:
            with open(self.filename, 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader)
                data = list(reader)
                if data:
                    last_id = int(data[-1][0])
                    return last_id + 1
                else:
                    return 1
        except FileNotFoundError:
            return 1


# პროგრამის გამშვები
def run_app():
    book_manager = BookManager("library.csv")
    print("Welcome to Book Manager!")
    while True:
        decision = input(
            "\nMain Menu\n1 - Add Book\n2 - Search Book\n3 - Display Books\n9 - Exit\nchoose (1,2,3 or 9): ")
        if decision == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            while not all(char.isalpha() or char.isspace() for char in author):
                print("Invalid Author, use only alphabetical letters")
                author = input("Enter book author: ")
            year = input("Enter book year: ")
            while True:
                if year.isdigit() and 1800 <= eval(year) <= datetime.now().year:
                    break
                print(f"Invalid input! year has to be an integer and less than {datetime.now().year}")
                year = input("Enter book year: ")
            book_manager.add_book(title, author, year)
        elif decision == "2":
            title = input("Enter book title to search: ")
            book_manager.search_book(title)

        elif decision == "3":
            book_manager.display_books()

        elif decision == "9":
            print("Thanks for using book manager!\nGoodbye...")
            break
        else:
            print("\nInvalid input entered! choose (1,2,3 or 9)")


run_app()
