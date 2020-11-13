import pytest

from flask import session

from watch_movies.authentication.services import AuthenticationException
from watch_movies.movie_lib import services as movie_library_services
from watch_movies.authentication import services as auth_services
from watch_movies.movie_lib.services import NonExistentMovieException
from watch_movies.domain.model import Movie, Genre, Director, Actor, Review, User


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'username': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('cj', '', b'Your username is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    client.post(
        '/authentication/register',
        data={'username': 'fmercury', 'password': '1234567890'}
    )
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


#def test_login(client, auth):
    # Check that we can retrieve the login page.
#    status_code = client.get('/authentication/login').status_code
#    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
#    response = auth.login()
#    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
#    with client:
#        client.get('/')
#        assert session['username'] == 'thorke'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200


def test_login_required_to_review(client):
    response = client.post('/review')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


#def test_review(client, auth):
    # Login a user.
#    auth.login()

    # Check that we can retrieve the comment page.
#    response = client.get('/review?movie=2')

#    response = client.post(
#        '/review',
#        data={'review': 'Who needs quarantine?', 'movie_id': 2}
#    )
#    assert response.headers['Location'] == 'http://localhost/movies_by_id?id=2&view_reviews_for=2'


@pytest.mark.parametrize(('review', 'messages'), (
        ('Who thinks Trump is a fuckwit?', (b'Your comment must not contain profanity')),
        ('Hey', (b'Your comment is too short')),
))
def test_review_with_invalid_input(client, auth, review, messages):
    #Login a user.
    auth.login()

    # Attempt to comment on an article.
    response = client.post(
        '/review',
        data={'review': review, 'movie_id': 2}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data

"""
def test_movies_without_id(client):
    # Check that we can retrieve the articles page.
    response = client.get('/movies_by_ids')
    assert response.status_code == 200

    # Check that without providing a date query parameter the page includes the first article.
    assert b'Guardian of the Galaxy' in response.data
"""
"""
def test_movies_with_id(client):
    # Check that we can retrieve the articles page.
    response = client.get('/movies_by_ids?id=2')
    assert response.status_code == 200

    # Check that all articles on the requested date are included on the page.
    assert b'Prometheus' in response.data


def test_movies_with_review(auth, client):
    auth.login()
    response = client.post(
                '/review',
                data={'review': 'Nice movie', 'movie_id': 2}
            )
    #Check that we can retrieve the articles page.
    response = client.get('/movies_by_ids?id=2&view_reviews_for=2')
    assert response.status_code == 200

    # Check that all comments for specified article are included on the page.
    assert b'Nice movie' in response.data


def test_movies_with_genre(client):
    # Check that we can retrieve the articles page.
    response = client.get('/movies_by_genres?genre=Action')
    assert response.status_code == 200

    # Check that all articles tagged with 'Health' are included on the page.
    assert b'Guardians of the Galaxy' in response.data
    assert b'Suicide Squad' in response.data
"""
