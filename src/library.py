import json
import os
from .book import Book
from .book import BookTitleError,BookAuthorError,GenerateIDError,BookStatusError,BookSearchFieldError,BookNotFoundError

class Library:
    """
    Класс для управления библиотекой книг.
    Внутренние переменные:
    book_valid_search_fields - список полей, по которым можно искать книги
    valid_book_statuses - список статусов книг (по условию "выдана" и "в наличии")
    """

    MAX_BOOK_COUNT = 10_000

    def __init__(self):
        """Инициализация библиотеки."""
        self.valid_book_statuses = ["выдана", "в наличии"]
        self.book_valid_search_fields = ["title","author","status"]
        self.books = self._load_books()

    def _load_books(self) -> list:
        """
        Загрузка книг из файла library.json.
        Если книг нет, возвращает пустой список
        """
        if os.path.exists("library.json"):
            with open("library.json", "r") as f:
                try:
                    return [Book(**book) for book in json.load(f)]
                except json.JSONDecodeError:
                    # Невалидный формат файла library.json
                    return []
        else:
            return []

    def _generate_book_id(self) -> int:
        """
        Генерирует уникальный ID книги (первое большее нуля число, которое еще не занято другими ID), возвращает ID.
        ID - целое число, большее нуля.
        Если книг нет, возвращает 1.
        Если невозможно генерировать ID вызывает исключение GenerateIDError
        """
        result = -1
        valid_new_book_id = [True]*(self.MAX_BOOK_COUNT+1) # массив с id, которые еще не заняты, индекс 0 - не учитывается
        for book in self.books:
            valid_new_book_id[book.id]=False
        for i in range(1,self.MAX_BOOK_COUNT+1):
            if valid_new_book_id[i]:
                result=i
                break
        if result==-1:
            raise GenerateIDError
        return result

    def _save_books(self):
        """Сохранение книг в файл library.json."""
        with open("library.json", "w") as f:
            json.dump([book.__dict__ for book in self.books], f, indent=4)


    def add_book(self, title: str, author: str, year: int) -> int:
        """
        Добавление книги в библиотеку.
        Возвращаем ID добавленной книги, если возникла ошибка - возвращает -1, выводит почему произошла ошибка
        """
        book_id = self._generate_book_id()
        book = Book(book_id, title, author, year)
        self.books.append(book)
        self._save_books()
        return book_id

    def delete_book(self, book_id: int) -> int:
        """
        Удаление книги из библиотеки.
        Возвращаем ID удаленной книги, если не нашли книгу с таким ID - возвращаем -1
        """
        for i, book in enumerate(self.books):
            if book.id == book_id:
                del self.books[i]
                self._save_books()
                return book_id
        return -1

    def search_book(self, query: str, field: str = "title") -> list:
        """
        Поиск книги по названию, автору или году издания.
        Возвращаем список найденных по фильтру книг, если не нашли - пустой список
        """
        results = []
        if not field in self.book_valid_search_fields:
            raise BookSearchFieldError(field)
        for book in self.books:
            if getattr(book, field) == query:
                results.append(book)
        return results

    def check_book_presence_by_id(self, book_id: int) -> bool:
        """Проверяем наличие книги по ID, если в наличии, возвращает True"""
        for book in self.books:
            if book.id == book_id:
                return True
        return False

    def get_all_books(self) -> list:
        """Возвращает все книги библиотеки"""
        return self.books

    def change_book_status(self, book_id: int, new_status: str):
        """
        Изменение статуса книги.
        Возвращает объект книги Book, статус которого поменяли. Если книга не найдена, возвращает None"""
        if not self.check_book_presence_by_id(book_id):
            raise BookNotFoundError(book_id)
        if new_status not in self.valid_book_statuses:
            raise BookStatusError(new_status)
        for book in self.books:
            if book.id == book_id:
                book.status = new_status
                self._save_books()
                return book

    def delete_all_books(self):
        ids = [book.id for book in self.books]
        for i in ids:
            self.delete_book(i)
        self._save_books()
        return len(ids)