import pytest

from watch_movies.domain.model import User, Director, Genre, Movie, Actor, Review, User, make_review
from watch_movies.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = in_memory_repo.add_user(User('Dave', '123456789'))

    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    in_memory_repo.add_user(User('fmercury', '8734gfe2058v'))
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()

    # Check that the query returned 1000 watch_movies.
    assert number_of_movies == 1000

"""
def test_repository_can_add_movie(in_memory_repo):
    movie = Movie(
        "TXXT", 2020
    )
    in_memory_repo.add_movie(movie)

    assert in_memory_repo.get_movie(1001) is movie
"""

def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)

    # Check that the movie has the expected title.
    assert movie.title == "Guardians of the Galaxy"
    assert movie.genres == [Genre("Action"), Genre("Adventure"), Genre("Sci-Fi")]
    assert movie.release_year == 2014
    assert movie.actors == [Actor("Chris Pratt"), Actor("Vin Diesel"), Actor("Bradley Cooper"), Actor("Zoe Saldana")]
    assert movie.director == Director("James Gunn")


def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1008)
    assert movie is None

"""
def test_repository_can_retrieve_movies_by_year(in_memory_repo):
    movies = in_memory_repo.get_movies_by_year(2005)

    # Check that the query returned 1 movie.
    assert len(movies) == 1
"""

def test_repository_does_not_retrieve_a_movie_when_there_are_no_movies_for_a_given_year(in_memory_repo):
    movies = in_memory_repo.get_movies_by_year(2021)
    assert len(movies) == 0

"""
def test_repository_can_get_first_movie(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    assert movie.title == 'Guardians of the Galaxy'


def test_repository_can_get_last_movie(in_memory_repo):
    movie = in_memory_repo.get_last_movie()
    assert movie.title == 'Nine Lives'
"""

def test_repository_can_get_movies_by_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_ids([2, 5, 6])

    assert len(movies) == 3
    assert movies[0].title == 'Prometheus'
    assert movies[1].title == "Suicide Squad"
    assert movies[2].title == 'The Great Wall'


def test_repository_does_not_retrieve_movie_for_non_existent_id(in_memory_repo):
    movies = in_memory_repo.get_movies_by_ids([2, 2000])

    assert len(movies) == 1
    assert movies[0].title == 'Prometheus'


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_ids([0, 2000])

    assert len(movies) == 0

"""
def test_repository_returns_movie_ids_for_existing_actor(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_actor('Chris Pratt')

    assert movie_ids == [1, 10, 39, 86, 385, 407, 697]
"""

def test_repository_returns_an_empty_list_for_non_existent_actor(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_actor('United States')

    assert len(movie_ids) == 0

"""
def test_repository_returns_movie_ids_for_existing_director(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_director('Adam McKay')

    assert movie_ids == [143, 361, 470, 936]
"""

def test_repository_returns_an_empty_list_for_non_existent_director(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_director('United States')

    assert len(movie_ids) == 0

"""
def test_repository_returns_movie_ids_for_existing_genre(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_genre('Sport')

    assert movie_ids == [195, 311, 338, 368, 378, 382, 494, 549, 575, 585, 587, 594, 597, 831, 850, 897, 936, 975]
"""

def test_repository_returns_an_empty_list_for_non_existent_genre(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_genre('United States')

    assert len(movie_ids) == 0


def test_repository_returns_id_of_previous_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(6)
    previous_id = in_memory_repo.get_id_of_previous_movie(movie)

    assert previous_id == 5


def test_repository_returns_none_when_there_are_no_previous_movies(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    previous_id = in_memory_repo.get_id_of_previous_movie(movie)

    assert previous_id is None


def test_repository_returns_id_of_next_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(3)
    next_id = in_memory_repo.get_id_of_next_movie(movie)

    assert next_id == 4


def test_repository_returns_none_when_there_are_no_subsequent_movies(in_memory_repo):
    movie = in_memory_repo.get_movie(2000)
    next_id = in_memory_repo.get_id_of_next_movie(movie)

    assert next_id is None


def test_repository_return_genres_of_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    genre = movie.genres
    assert genre == [Genre('Action'), Genre('Adventure'), Genre('Sci-Fi')]


def test_repository_return_director_of_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    director = movie.director
    assert director == Director('James Gunn')


def test_repository_return_actors_of_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    actor = movie.actors
    assert actor == [Actor('Chris Pratt'), Actor('Vin Diesel'), Actor('Bradley Cooper'), Actor('Zoe Saldana')]


def test_repository_can_add_a_review(in_memory_repo):
    user = User('thorke', 'abcd1A23')
    in_memory_repo.add_user(user)
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(2)
    review = make_review(movie, "Love it!!", user)
    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()


def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    review = Review(movie, "TT", None)

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_does_not_add_a_review_without_an_movie_properly_attached(in_memory_repo):
    user = User('thorke', 'abcd1A23')
    in_memory_repo.add_user(user)
    user = in_memory_repo.get_user('thorke')
    review = Review(None, "Love it!!", user)

    with pytest.raises(RepositoryException):
        # Exception expected because the movie doesn't refer to the review.
        in_memory_repo.add_review(review)


def test_repository_can_retrieve_comments(in_memory_repo):
    user = User('thorke', 'abcd1A23')
    in_memory_repo.add_user(user)
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(2)
    review = make_review(movie, "Love it!!",user)
    in_memory_repo.add_review(review)
    assert len(in_memory_repo.get_reviews()) == 1
