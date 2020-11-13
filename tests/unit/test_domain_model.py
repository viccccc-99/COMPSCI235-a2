from datetime import date

from watch_movies.domain.model import Director, Genre, Movie, Actor, Review, User, make_review

import pytest


@pytest.fixture()
def movie():
    return Movie(
        "Moana", 2016
    )


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def actor():
    return Actor("Auli'i Cravalho")


@pytest.fixture()
def director():
    return Director("Ron Clements")


@pytest.fixture()
def genre():
    return Genre("Cartoon")


def test_user_construction(user):
    assert user.username == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<dbowie>'

    for review in user.reviews:
        # User should have an empty list of Comments after construction.
        assert False


def test_movie_construction(movie):
    assert movie.id is None
    assert movie.release_year == 2016
    assert movie.title == "Moana"
    movie.add_actor(Actor("Auli'i Cravalho"))
    assert len(movie.actors) == 1
    movie.remove_actor(Actor("Auli'i Cravalho"))
    assert len(movie.actors) == 0
    movie.add_genre(Genre("Action"))
    assert len(movie.genres) == 1
    movie.remove_genre(Genre("Action"))
    assert len(movie.genres) == 0
    assert movie.director is None
    assert movie.runtime_minutes is None

    assert repr(
        movie) == '<Moana, 2016>'


def test_movie_less_than_operator():
    article_1 = Movie(
        "IT", 2018
    )

    article_2 = Movie(
        "Moana", 2016
    )

    assert article_1 < article_2


def test_actor_construction(actor):
    assert actor.actor_full_name == "Auli'i Cravalho"

    actor.add_actor_colleague(Actor("Dwayne Johnson"))
    assert actor.check_if_this_actor_worked_with(Actor("Dwayne Johnson"))


def test_make_reviews_establishes_relationships(movie, user):
    review_text = "Excellent!"
    review = make_review(movie, review_text,user)
    # Check that the User object knows about the review.
    assert review in user.reviews

    # Check that the review knows about the User.
    assert review.user is user

    # Check that movie knows about the review.
    assert review in movie.reviews

    # Check that the review knows about the movie.
    assert review.movie is movie
