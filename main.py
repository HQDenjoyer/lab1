import json
import os


def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')


class Book:
    def __init__(self, name, author, year, genre):
        self.name = name
        self.author = author
        self.year = year
        self.genre = genre
        self.index = None

    def assign_index(self, index):
        self.index = index


class Library:
    def __init__(self):
        self.books = []
        self.deleted_books = []
        self.current_index = 1

    def search_book(self, name):
        found_books = []
        for book in self.books:
            if book.name.lower() == name.lower():
                found_books.append(book)
        return found_books

    def add_book(self, book):
        if not book.name.strip():
            print("Ошибка: Название книги не может быть пустым.")
            return
        book.assign_index(self.current_index)
        self.current_index += 1
        self.books.append(book)

    def display_books(self):
        if not self.books:
            print("В библиотеке нет книг.")
        else:
            for book in self.books:
                print(
                    f"Индекс: {book.index}, Название: {book.name}, Автор: {book.author}, Год издания: {book.year}, Жанр: {book.genre}")

    def delete_book(self, index):
        found_book = None
        for book in self.books:
            if book.index == index:
                found_book = book
                break
        if found_book:
            self.books.remove(found_book)
            self.deleted_books.append(found_book)
            print("Книга успешно перемещена в архив.")
        else:
            print("Ошибка: Книга с таким индексом не найдена.")

    def update_book(self, index, name, author, year, genre):
        for book in self.books:
            if book.index == index:
                book.name = name
                book.author = author
                book.year = year
                book.genre = genre
                print("Книга успешно обновлена.")
                return
        print("Ошибка: Книга с таким индексом не найдена.")

    def display_deleted_books(self):
        if not self.deleted_books:
            print("В архиве нет книг.")
        else:
            for book in self.deleted_books:
                print(
                    f"Индекс: {book.index}, Название: {book.name}, Автор: {book.author}, Год издания: {book.year}, Жанр: {book.genre}")

    def permanently_delete_book(self, index):
        found_book = None
        for book in self.deleted_books:
            if book.index == index:
                found_book = book
                break
        if found_book:
            self.deleted_books.remove(found_book)
            print("Книга успешно удалена из архива.")
        else:
            print("Ошибка: Книга с таким индексом не найдена.")

    def restore_book(self, index):
        found_book = None
        for book in self.deleted_books:
            if book.index == index:
                found_book = book
                break
        if found_book:
            self.deleted_books.remove(found_book)
            self.books.append(found_book)
            print("Книга успешно восстановлена.")
        else:
            print("Ошибка: Книга с таким индексом не найдена.")


def save_library(library):
    books_data = [{"index": book.index, "name": book.name, "author": book.author, "year": book.year, "genre": book.genre} for book in library.books]
    deleted_books_data = [{"index": book.index, "name": book.name, "author": book.author, "year": book.year, "genre": book.genre} for book in library.deleted_books]
    library_data = {"current_index": library.current_index, "books": books_data, "deleted_books": deleted_books_data}
    with open("library.json", "w") as file:
        json.dump(library_data, file)


def load_library():
    try:
        with open("library.json", "r") as file:
            data = json.load(file)
            library = Library()
            library.current_index = data.get("current_index", 1)
            books_data = data.get("books", [])
            deleted_books_data = data.get("deleted_books", [])
            for book_info in books_data:
                book = Book(book_info['name'], book_info['author'], book_info['year'], book_info['genre'])
                book.assign_index(book_info['index'])
                library.books.append(book)
            for book_info in deleted_books_data:
                book = Book(book_info['name'], book_info['author'], book_info['year'], book_info['genre'])
                book.assign_index(book_info['index'])
                library.deleted_books.append(book)
            return library
    except FileNotFoundError:
        return Library()


def main():
    global auth_choice
    library = load_library()
    authorized = False

    while not authorized:
        print("\nМеню авторизации")
        print("1. Авторизоваться")
        print("2. Войти как гость")
        auth_choice = input("Выберите опцию: ")
        clear_screen()

        if auth_choice == '1':
            login = input("Введите логин: ")
            password = input("Введите пароль: ")
            if login == 'admin' and password == 'admin':
                authorized = True
                print("Вы успешно авторизовались.")
                clear_screen()
            else:
                clear_screen()
                print("Неправильный логин или пароль. Попробуйте еще раз.\n")
        elif auth_choice == '2':
            authorized = True
            print("Вы вошли как гость.")
            clear_screen()
        else:
            print("Недопустимый выбор.")
            clear_screen()

    while authorized:
        if auth_choice == '1':
            print("\nСистема управления библиотекой")
            print("1. Добавить книгу")
            print("2. Показать книги")
            print("3. Удалить книгу")
            print("4. Обновить книгу")
            print("5. Показать удаленные книги")
            print("6. Поиск книги по названию")
            print("7. Выход")
        else:
            print("1. Показать книги")
            print("2. Выход")

        choice = input("Введите ваш выбор: ")

        if choice == '1':
            if auth_choice == '1':
                clear_screen()
                name = input("Введите название книги: ")
                if not name.strip():
                    print("Ошибка: Название книги не может быть пустым.")
                    continue
                author = input("Введите имя автора: ")
                while True:
                    try:
                        year = int(input("Введите год издания: "))
                        if not (400 <= year <= 2500):
                            print("Ошибка: Некорректная дата.")
                            continue
                        break
                    except ValueError:
                        print("Ошибка: Некорректная дата.")
                genre = input("Введите жанр книги: ")
                book = Book(name, author, year, genre)
                library.add_book(book)
                save_library(library)
                print("Книга успешно добавлена.")
            else:
                library.display_books()
        elif choice == '2':
            clear_screen()
            if auth_choice == '1':
                library.display_books()
            else:
                break
        elif choice == '3':
            clear_screen()
            while True:
                try:
                    index = input(
                        "Чтобы вернуться в меню, оставьте поле пустым или напишите что угодно кроме цифр и нажмите 'Enter'.\nВведите номер книги для удаления: ")
                    if not index.strip():
                        clear_screen()
                        break
                    index = int(index)
                    library.delete_book(index)
                    save_library(library)
                except ValueError:
                    clear_screen()
                    break
        elif choice == '4':
            clear_screen()
            while True:
                try:
                    index = int(input("Чтобы вернуться в меню оставьте поле "
                                      "пустым или напишите что угодно кроме цифр и нажмите 'Enter"
                                      "\nВведите номер книги для обновления:"))
                    name = input("Введите новое название: ")
                    if not name.strip():
                        print("Ошибка: Название книги не может быть пустым.")
                        continue
                    author = input("Введите новое имя автора: ")
                    while True:
                        try:
                            year = int(input("Введите новый год издания: "))
                            if not (400 <= year <= 2500):
                                print("Ошибка: Некорректная дата.")
                                continue
                            break
                        except ValueError:
                            print("Ошибка: Некорректная дата.")
                    genre = input("Введите новый жанр: ")
                    library.update_book(index, name, author, year, genre)
                    save_library(library)
                    clear_screen()
                except ValueError:
                    clear_screen()
                    break
        elif choice == '5':
            clear_screen()
            library.display_deleted_books()
            if library.deleted_books:
                try:
                    inner_choice = input("Введите 'в' чтобы восстановить книгу или 'у' чтобы удалить книгу: ")
                    if inner_choice.lower() == 'в':
                        index = int(input("Введите номер книги для восстановления: "))
                        library.restore_book(index)
                    elif inner_choice.lower() == 'у':
                        index = int(input("Введите номер книги для удаления: "))
                        library.permanently_delete_book(index)
                    else:
                        print("Ошибка: Недопустимый выбор.")
                    save_library(library)
                except ValueError:
                    print("Ошибка: Некорректный номер книги")
        elif choice == '6':
            clear_screen()
            name = input("Введите название книги для поиска: ")
            found_books = library.search_book(name)
            if found_books:
                print("Найденные книги:")
                for book in found_books:
                    print(
                        f"Индекс: {book.index}, Название: {book.name}, Автор: {book.author}, Год издания: {book.year}, Жанр: {book.genre}")
            else:
                print("Книги с таким названием не найдено.")
        elif choice == '7':
            clear_screen()
            save_library(library)
            print("Завершение работы.")
            break
        else:
            clear_screen()
            print("Недопустимый выбор.")



if __name__ == "__main__":
    main()