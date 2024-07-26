from src.book import BookTitleError,BookAuthorError,GenerateIDError,BookStatusError,BookSearchFieldError,BookNotFoundError
from src.library import Library

"""
Хранение данных происходит в json формате в нескольких файлах:
Файл "book_ids.json" содержит пары (id книги, название файла с информацией о книге)
Файл с информацией о книге записывается в директории "books_info" под названием "book_<id книги>.json"
Такая система хранения данных реализована на случай наличия огромного количества книг в библиотеке
и на случай добавления дополнительных параметров книги (дата добавления в базу, адрес хранения, и тд)

Проблема в том чтобы быстро просматривать файл при использовании функции поиска
"""


def main():
    """Главная функция."""
    library = Library()
    while True:
        print("Меню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Введите номер операции: ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            try:
                year = int(input("Введите год издания: "))
                # Пытаемся создать и добавить книгу в библиотеку
                result = library.add_book(title, author, year)
            except BookTitleError as bte:
                # Некорректное название
                print(
                    f"В названии книги должно быть менее {bte.max_len} символов, сейчас {len(bte.title)} символов")
            except BookAuthorError as bae:
                # Некорректное имя автора
                print(
                    f"Имя автора должно занимать менее {bae.max_len} символов, сейчас {len(bae.author)} символов")
            except GenerateIDError:
                # Не получилось добавить книгу, так как каталог книг переполнена
                print("Переполнение библиотеки книгами")
            except ValueError:
                # Введена строка вместо числа для year
                print("Год выпуска должен быть числом!")
            else:
                print(f"Книга с ID {result} была добавлена!")

        elif choice == '2':
            try:
                book_id = int(input("Введите ID книги: "))
                result = library.delete_book(book_id)
                if result!=-1:
                    print("Книга удалена!")
                else:
                    print("Такая книга не найдена!")
            except ValueError:
                # Введена строка вместо числа в качестве ID
                print("ID должно быть числом!")

        elif choice == '3':
            try:
                search_field = input("Введите поле для поиска (title, author, year): ")
                query = input("Введите значение для поиска: ")
                search_result = library.search_book(query, search_field)
                if search_result:
                    print("Найденные книги:")
                    for book in search_result:
                        print(book)
                else:
                    print("Книги не найдены.")
            except BookSearchFieldError:
                book_valid_search_fields = '"'+ '", "'.join(library.book_valid_search_fields)+'"'
                print(f"Параметром книги для поиска для поиска могут быть только: {book_valid_search_fields}")

        elif choice == '4':
            books = library.get_all_books()
            if books:
                print("Список книг:")
                for book in books:
                    print(book)
            else:
                print("Библиотека пуста.")

        elif choice == '5':
            try:
                book_id = int(input("Введите ID книги: "))
                new_status = input("Введите новый статус - 'в наличии' или 'выдана': ")
                status_changed_book = library.change_book_status(book_id, new_status)
            except BookNotFoundError as book_not_found_error:
                print(f"Книга с ID {book_not_found_error.wrong_id} не найдена в библиотеке!")
            except BookStatusError as book_status_error:
                valid_book_statuses='"' + '", "'.join(library.valid_book_statuses) + '"'
                print(
                    f"Некорректный статус: '{book_status_error.wrong_status}', "
                    f"правильным статусом может быть одно из значений: {valid_book_statuses}")
            else:
                print("Статус книги изменен! Информация об этой книге:")
                print(status_changed_book)


        elif choice == '6':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 6.")

if __name__ == "__main__":
    main()
