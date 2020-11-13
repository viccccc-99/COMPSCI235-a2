import pytest

from watch_movies.authentication.services import AuthenticationException
from watch_movies.movie_lib import services as movie_lib_services
from watch_movies.authentication import services as auth_services
from watch_movies.movie_lib.services import NonExistentMovieException
from watch_movies.domain.model import Movie, Genre, Director, Actor, Review, User


def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'thorke'
    password = 'abcd1A23'
    auth_services.add_user(username, password, in_memory_repo)
    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_review(in_memory_repo):
    movie_id = 3
    review_text = 'Niceee!'
    username = 'fmercury'
    password = '123456789'
    auth_services.add_user(username, password, in_memory_repo)

    # Call the service layer to add the comment.
    movie_lib_services.add_review(movie_id, review_text, username, in_memory_repo)

    # Retrieve the comments for the article from the repository.
    reviews_as_dict = movie_lib_services.get_reviews_for_movie(movie_id, in_memory_repo)

    # Check that the comments include a comment with the new comment text.
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
        None) is not None


def test_cannot_add_review_for_non_existent_movie(in_memory_repo):
    movie_id = 9000
    review_text = 'Niceee!'
    username = 'fmercury'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movie_lib_services.NonExistentMovieException):
        movie_lib_services.add_review(movie_id, review_text, username, in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    movie_id = 3
    review_text = 'Niceee!'
    username = 'gmichael'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movie_lib_services.UnknownUserException):
        movie_lib_services.add_review(movie_id, review_text, username, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie_id = 2

    movie_as_dict = movie_lib_services.get_movie(movie_id, in_memory_repo)

    assert movie_as_dict['id'] == movie_id
    assert movie_as_dict['year'] == 2012
    assert movie_as_dict['title'] == 'Prometheus'
    assert movie_as_dict['description'] == 'Following clues to the origin of mankind, a team finds a structure on a distant moon, but they soon realize they are not alone.'
    assert movie_as_dict['actors'] == [Actor("Noomi Rapace"), Actor("Logan Marshall-Green"),Actor("Michael Fassbender"), Actor("Charlize Theron")]
    assert movie_as_dict['genres'] == [Genre("Adventure"), Genre("Mystery"), Genre("Sci-Fi")]
    assert movie_as_dict['director'] == Director("Ridley Scott")
    assert len(movie_as_dict['reviews']) == 0


def test_cannot_get_movie_with_non_existent_id(in_memory_repo):
    movie_id = 9000

    # Call the service layer to attempt to retrieve the Movie.
    with pytest.raises(movie_lib_services.NonExistentMovieException):
        movie_lib_services.get_movie(movie_id, in_memory_repo)

"""
def test_get_first_movie(in_memory_repo):
    movie_as_dict = movie_lib_services.get_first_movie(in_memory_repo)

    assert movie_as_dict['id'] == 1


def test_get_last_movie(in_memory_repo):
    movie_as_dict = movie_lib_services.get_last_movie(in_memory_repo)

    assert movie_as_dict['id'] == 1000


def test_get_movies_by_id(in_memory_repo):
    target_id = 1

    movies_as_dict, prev_id, next_id = movie_lib_services.get_movies_by_ids(target_id, in_memory_repo)

    assert len(movies_as_dict) == 1
    assert movies_as_dict[0]['id'] == 1

    assert prev_id is None
    assert next_id == 2


def test_get_movies_by_id_with_non_existent_id(in_memory_repo):
    target_id = 9000

    movies_as_dict, prev_id, next_id = movie_lib_services.get_movies_by_ids(target_id, in_memory_repo)

    # Check that there are no articles dated 2020-03-06.
    assert len(movies_as_dict) == 0
"""

def test_get_movies_by_ids(in_memory_repo):
    target_movie_ids = [5, 6, 9000]
    movies_as_dict = movie_lib_services.get_movies_by_ids(target_movie_ids, in_memory_repo)

    # Check that 2 articles were returned from the query.
    assert len(movies_as_dict) == 2

    # Check that the article ids returned were 5 and 6.
    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert {5, 6}.issubset(movie_ids)


def test_get_reviews_for_movie(in_memory_repo):
    username = 'fmercury'
    password = 'abcd1A23'
    auth_services.add_user(username, password, in_memory_repo)
    movie_lib_services.add_review(1, "Nicee", username, in_memory_repo)
    reviews_as_dict = movie_lib_services.get_reviews_for_movie(1, in_memory_repo)

    # Check that 2 comments were returned for article with id 1.
    assert len(reviews_as_dict) == 1

    # Check that the comments relate to the article whose id is 1.
    movie_ids = [review['movie_id'] for review in reviews_as_dict]
    movie_ids = set(movie_ids)
    assert 1 in movie_ids and len(movie_ids) == 1


def test_get_reviews_for_non_existent_movie(in_memory_repo):
    with pytest.raises(NonExistentMovieException):
        reviews_as_dict = movie_lib_services.get_reviews_for_movie(9000, in_memory_repo)


def test_get_reviews_for_movie_without_reviews(in_memory_repo):
    reviews_as_dict = movie_lib_services.get_reviews_for_movie(7, in_memory_repo)
    assert len(reviews_as_dict) == 0
