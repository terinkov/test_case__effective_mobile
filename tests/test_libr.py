import unittest
from src.library import Library
# from unittest.mock import patch
from src.book import Book

class TestLibrary(unittest.TestCase):

    def setUp(self):
        """Настройка для каждого теста."""
        self.library = Library()

    def test_delete_all_books(self):
        self.library.add_book("Название книги", "Автор книги", 1990)
        self.library.add_book("Название книги 2", "Автор книги 2", 1991)
        self.library.delete_all_books()
        self.assertEqual(len(self.library.books), 0) # Проверка что все книги удалились

    def test_add_book(self):
        self.library.delete_all_books()
        """Проверка добавления книги."""
        self.library.add_book("Название книги", "Автор книги", 2023)
        self.assertEqual(len(self.library.books), 1) # Проверка что книга добавилась
        self.assertEqual(self.library.books[0].id, 1) # Проверка что ID этой книги 1

    def test_delete_book(self):
        self.library.delete_all_books()
        """Проверка удаления книги."""
        self.library.add_book("Название книги", "Автор книги", 2023)
        self.library.delete_book(1)
        self.assertEqual(len(self.library.books), 0)




if __name__ == '__main__':
    unittest.main()