import abc
from typing import List

from watch_movies.domain.model import Director, Genre, Movie, Actor, Review, User

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds a movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, id: int) -> Movie:
        """ Returns movie with id from the repository.

        If there is no movie with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_year(self, target_year: int) -> List[Movie]:
        """ Returns a list of watch_movies that were released on target_year.
        If there are no watch_movies in the given year, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self):
        """ Returns the number of watch_movies in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self) -> Movie:
        """ Returns the first movie, ordered by date, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self) -> Movie:
        """ Returns the last movie, ordered by date, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_ids(self, id_list):
        """ Returns a list of movie_library, whose ids match those in id_list, from the repository.
        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_for_actor(self, actor_name: str):
        """ Returns a list of ids representing movie_library that have actor.
        If there are movie_library that are tagged by actor_name, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_for_director(self, director_name: str):
        """ Returns a list of ids representing movie_library that have Director.
        If there are movie_library that are tagged by actor_name, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_for_genre(self, genre_name: str):
        """ Returns a list of ids representing movie_library that have Genre.
        If there are movie_library that are tagged by Genre_name, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_id_of_previous_movie(self, movie: Movie):
        """ Returns the id of an Article that immediately precedes article.

        If movie is the first Article in the repository, this method returns None because there are no watch_movies
        on a previous date.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_id_of_next_movie(self, movie: Movie):
        """ Returns the id of an movie that immediately follows article.

        If article is the last movie in the repository, this method returns None because there are no watch_movies
        on a later date.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """ Adds a genre to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """ Returns the genres stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a review to the repository.

        If the review doesn't have bidirectional links with an movie and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.movie is None or review not in review.movie.reviews:
            raise RepositoryException('Review not correctly attached to a Movie')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the reviews stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_director(self) -> List[Director]:
        """returns the director stored in the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_actors(self) -> List[Actor]:
        """returns the actors stored in the repository"""
        raise NotImplementedError
