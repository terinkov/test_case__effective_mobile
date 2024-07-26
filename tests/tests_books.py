import unittest
from src.book import Book, BookTitleError, BookAuthorError, GenerateIDError, BookStatusError, BookSearchFieldError, BookNotFoundError

class TestBook(unittest.TestCase):

    def test_book_initialization_valid(self):
        """Проверка инициализации книги с корректными данными."""
        book = Book(1, "Название книги", "Автор книги", 2023)
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "Название книги")
        self.assertEqual(book.author, "Автор книги")
        self.assertEqual(book.year, 2023)
        self.assertEqual(book.status, "в наличии")

    def test_book_initialization_invalid_title(self):
        """Проверка инициализации книги с некорректным (слишком длинным) названием."""
        long_book_name = "0"*256
        with self.assertRaises(BookTitleError):
            Book(1, long_book_name, "Автор книги", 2023)

    def test_book_initialization_invalid_author(self):
        """Проверка инициализации книги с некорректным (слишком длинным именем) автором."""
        long_author_name = "0"*256
        with self.assertRaises(BookAuthorError):
            Book(1, "Название книги", long_author_name, 2023)

    def test_validate_title_valid(self):
        """Проверка метода validate_title с корректным названием."""
        book = Book(1, "Название книги", "Автор книги", 2023)
        book.validate_title()  # Не должно возникнуть исключений

    def test_validate_title_invalid(self):
        """Проверка метода validate_title с некорректным названием."""
        book = Book(1, "Очень длинное название книги, которое превышает допустимую длину", "Автор книги", 2023)
        with self.assertRaises(BookTitleError):
            book.validate_title()

    def test_validate_author_valid(self):
        """Проверка метода validate_author с корректным автором."""
        book = Book(1, "Название книги", "Автор книги", 2023)
        book.validate_author()  # Не должно возникнуть исключений

    def test_validate_author_invalid(self):
        """Проверка метода validate_author с некорректным автором."""
        book = Book(1, "Название книги", "Очень длинное имя автора, которое превышает допустимую длину", 2023)
        with self.assertRaises(BookAuthorError):
            book.validate_author()

    def test_str_representation(self):
        """Проверка строкового представления книги."""
        book = Book(1, "Название книги", "Автор книги", 2023)
        expected_str = "ID: 1, Название: Название книги, Автор: Автор книги, Год: 2023, Статус: in_stock"
        self.assertEqual(str(book), expected_str)


if __name__ == '__main__':
    unittest.main()
