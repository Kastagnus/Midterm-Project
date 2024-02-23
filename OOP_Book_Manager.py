'''
პროგრამა წარმოადგენს წიგნების მენეჯერს. პროგრამის გამოძახების დროს გამოდის მენიუ სადაც მომხმარებელი ირჩევს
წიგნის დამატებას, წიგნის ძებნას ან წიგნების სრული სიის ჩვენებას
პროგრამა მუშაობს მანამ სანამ მომხმარებელი არ მიმართავს Exit ბრძანებს ღილაკით 9

'''

# წიგნის კლასი ატრიბუტებით: სათაურით, ავტორითა და წიგნის წლით
class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"'{self.title}' by {self.author} ({self.year})"


# წიგნების მენეჯერ კლასი მეთოდებით 1.წიგნის დამატება 2. წიგნის ძებნა 3. წიგნების სრული სიის გამოტანა
class BookManager:

    def __init__(self):
        self.books = []

    def add_book(self, title, author, year):
        book = Book(title, author, year)
        self.books.append(book)
        print(f"\nBook added: {book}")

    def search_book(self, title):
        for book in self.books:
            if book.title == title:
                print(f"\nBook found: {book}")
                return True
        else:
            print("\nBook not found")
            return False

    def display_books(self):

        if self.books == []:
            print("No books in library yet! ")
        i = 1
        print("All books in library:")
        for book in self.books:
            print(f"\n\t{i} - {book}")
            i += 1


# პროგრამის გამშვები
def run_app():
    book_manager = BookManager()
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
                if year.isdigit() and int(year) < 2024:
                    break
                print("Invalid input! year has to be an integer and less than 2024")
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
