import pytest

class TestBooksCollector:

    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2
        assert 'Гордость и предубеждение и зомби' in collector.get_books_genre()
        assert 'Что делать, если ваш кот хочет вас убить' in collector.get_books_genre()

    def test_add_new_book_add_same_book_twice(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Гордость и предубеждение и зомби')
        assert len(collector.get_books_genre()) == 1

    @pytest.mark.parametrize("book_name", [
        'Валидное название книги',
        'x' * 40
    ])
    def test_add_new_book_valid_name_length(self, collector, book_name):
        collector.add_new_book(book_name)
        assert book_name in collector.get_books_genre()

    @pytest.mark.parametrize("book_name", [
        '',
        'x' * 41
    ])
    def test_add_new_book_invalid_name_length(self, collector, book_name):
        collector.add_new_book(book_name)
        assert book_name not in collector.get_books_genre()

    def test_set_book_genre_for_existing_book(self, collector):
        collector.add_new_book('Book1')
        collector.set_book_genre('Book1', 'Ужасы')
        assert collector.get_book_genre('Book1') == 'Ужасы'

    def test_set_book_genre_for_non_existing_book(self, collector):
        collector.set_book_genre('NonExistingBook', 'Ужасы')
        assert collector.get_book_genre('NonExistingBook') is None

    def test_set_book_genre_invalid_genre(self, collector):
        collector.add_new_book('Book1')
        collector.set_book_genre('Book1', 'Роман')
        assert collector.get_book_genre('Book1') == ''

    def test_get_book_genre_no_genre_set(self, collector):
        collector.add_new_book('Book1')
        assert collector.get_book_genre('Book1') == ''

    def test_get_book_genre_non_existing_book(self, collector):
        assert collector.get_book_genre('NonExistingBook') is None

    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book('Book1')
        collector.set_book_genre('Book1', 'Ужасы')
        collector.add_new_book('Book3')
        collector.set_book_genre('Book3', 'Ужасы')
        books = collector.get_books_with_specific_genre('Ужасы')
        assert 'Book1' in books
        assert 'Book3' in books
        assert len(books) == 2

    def test_get_books_with_specific_genre_no_books(self, collector):
        collector.add_new_book('Book1')
        collector.set_book_genre('Book1', 'Фантастика')
        books = collector.get_books_with_specific_genre('Ужасы')
        assert books == []

    def test_get_books_with_specific_genre_invalid_genre(self, collector):
        collector.add_new_book('Book1')
        collector.set_book_genre('Book1', 'Фантастика')
        books = collector.get_books_with_specific_genre('Роман')
        assert books == []

    def test_get_books_genre(self, collector):
        collector.add_new_book('Book1')
        collector.set_book_genre('Book1', 'Фантастика')
        collector.add_new_book('Book2')
        collector.set_book_genre('Book2', 'Ужасы')
        expected = {'Book1': 'Фантастика', 'Book2': 'Ужасы'}
        assert collector.get_books_genre() == expected

    def test_get_books_for_children_positive(self, collector):
        collector.add_new_book('Book1')
        collector.set_book_genre('Book1', 'Фантастика')
        collector.add_new_book('Book3')
        collector.set_book_genre('Book3', 'Мультфильмы')
        books_for_children = collector.get_books_for_children()
        assert 'Book1' in books_for_children
        assert 'Book3' in books_for_children

    def test_get_books_for_children_negative(self, collector):
        collector.add_new_book('Book2')
        collector.set_book_genre('Book2', 'Ужасы')
        books_for_children = collector.get_books_for_children()
        assert 'Book2' not in books_for_children

    def test_add_book_in_favorites(self, collector):
        collector.add_new_book('Book1')
        collector.add_book_in_favorites('Book1')
        assert 'Book1' in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_duplicate(self, collector):
        collector.add_new_book('Book1')
        collector.add_book_in_favorites('Book1')
        collector.add_book_in_favorites('Book1')
        assert collector.get_list_of_favorites_books().count('Book1') == 1

    def test_add_book_in_favorites_non_existing_book(self, collector):
        collector.add_book_in_favorites('NonExistingBook')
        assert 'NonExistingBook' not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book('Book1')
        collector.add_book_in_favorites('Book1')
        collector.delete_book_from_favorites('Book1')
        assert 'Book1' not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_not_in_favorites(self, collector):
        collector.add_new_book('Book1')
        collector.delete_book_from_favorites('Book1')
        assert 'Book1' not in collector.get_list_of_favorites_books()

    def test_get_list_of_favorites_books(self, collector):
        collector.add_new_book('Book1')
        collector.add_new_book('Book2')
        collector.add_book_in_favorites('Book1')
        favorites = collector.get_list_of_favorites_books()
        assert favorites == ['Book1']
