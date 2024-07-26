class Book:
    """Класс для представления книги.

    Параметры класса:
    id - уникальный идентификатор книги
    title - название, длина от 0 до 256 символов
    author - автор, длина от 0 до 256 символов
    year - год выпуска, любое число
    status - выдана или в наличии
    """

    MAX_TITLE_LENGHT = 256
    MAX_AUTHOR_LENGHT = 256

    def __init__(self, id: int, title: str, author: str, year: int, status: str = "в наличии"):
        """Инициализация объекта книги."""
        self.id = id  # Генерация уникального id
        self.title = title
        self.author = author
        self.year = year
        self.status = status
        self.validate_title()
        self.validate_author()

    def __str__(self):
        """Возвращает строковое представление книги."""
        return f"ID: {self.id}, Название: {self.title}, Автор: {self.author}, Год: {self.year}, Статус: {self.status}"

    def validate_title(self):
        if len(self.title) >= self.MAX_TITLE_LENGHT:
            raise BookTitleError(self.title, self.MAX_TITLE_LENGHT)

    def validate_author(self):
        if len(self.author) >= self.MAX_AUTHOR_LENGHT:
            raise BookAuthorError(self.title, self.MAX_AUTHOR_LENGHT)


class BookTitleError(ValueError):
    def __init__(self, title, max_length):
        self.title = title
        self.max_len = max_length


class BookAuthorError(ValueError):
    def __init__(self, author, max_length):
        self.author = author
        self.max_len = max_length


class GenerateIDError(IndexError):
    pass


class BookStatusError(AttributeError):
    def __init__(self, wrong_status):
        self.wrong_status = wrong_status


class BookSearchFieldError(ValueError):
    def __init__(self, wrond_field):
        self.wrong_field = wrond_field


class BookNotFoundError(ValueError):
    def __init__(self, wrond_id):
        self.wrong_id = wrond_id
