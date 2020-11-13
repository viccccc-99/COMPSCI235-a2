import csv
import os
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from watch_movies.adapters.repository import AbstractRepository, RepositoryException
from watch_movies.domain.model import Director, Genre, Movie, Actor, Review, User


class MemoryRepository(AbstractRepository):
    # Movies ordered by year, not id. id is assumed unique.

    def __init__(self):
        self._movies = list()
        self._movies_index = dict()
        self._genres = list()
        self._users = list()
        self._reviews = list()
        self._directors = list()
        self._actors = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        for user in self._users:
            if user.username == username:
                return user
        return None

    def add_movie(self, movie: Movie):
        insort_left(self._movies, movie)
        self._movies_index[movie.id] = movie

    def get_movie(self, id: int) -> Movie:
        movie = None

        try:
            movie = self._movies_index[id]
        except KeyError:
            pass  # Ignore exception and return None.

        return movie

    def get_movies_by_year(self, target_year: int) -> List[Movie]:

        matching_movies = list()
        try:
            for movie in self._movies:
                if movie.release_year == target_year:
                    matching_movies.append(movie)
        except ValueError:
            # No articles for specified date. Simply return an empty list.
            pass
        return matching_movies

    def get_number_of_movies(self):
        return len(self._movies)

    def get_first_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[0]
        return movie

    def get_last_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[-1]
        return movie

    def get_movies_by_ids(self, id_list):
        # Strip out any ids in id_list that don't represent movie ids in the repository.
        existing_ids = [ids for ids in id_list if ids in self._movies_index]


        # Fetch the watch_movies.
        movies = [self._movies_index[ids] for ids in existing_ids]
        return movies

    def get_movie_ids_for_actor(self, actor_name: str):
        # Linear search, to find the first occurrence of a Actor with the name actor_name.
        actor = next((actor for actor in self._actors if actor.actor_full_name == actor_name), None)

        # Retrieve the ids of watch_movies associated with the actor.
        if actor is not None:
            movie_ids = [movie.id for movie in self._movies if actor in movie.actors]
        else:
            # No Actor with name actor_name, so return an empty list.
            movie_ids = list()
        return movie_ids

    def get_movie_ids_for_genre(self, genre_name: str):
        # Linear search, to find the first occurrence of a genre with the name genre_name.
        genre = next((genre for genre in self._genres if genre.genre_name == genre_name), None)

        # Retrieve the ids of watch_movies associated with the genre.
        if genre is not None:
            movie_ids = [movie.id for movie in self._movies if genre in movie.genres]
        else:
            # No Actor with name actor_name, so return an empty list.
            movie_ids = list()
        return movie_ids

    def get_movie_ids_for_director(self, director_name: str):
        # Linear search, to find the first occurrence of a director with the name director_name.
        director = next((director for director in self._directors if director.director_full_name == director_name),
                        None)

        # Retrieve the ids of watch_movies associated with the director.
        if director is not None:
            movie_ids = [movie.id for movie in self._movies if director in movie.director]
        else:
            # No Actor with name director_name, so return an empty list.
            movie_ids = list()
        return movie_ids

    def get_id_of_previous_movie(self, movie: Movie):
        previous_id = None
        if movie.id > 1:
            previous_id = movie.id - 1
        else:
            return None
        return previous_id

    def get_id_of_next_movie(self, movie: Movie):
        next_id = None
        if movie is None:
            return None
        elif movie.id < len(self._movies):
            next_id = movie.id + 1
        return next_id

    def add_genre(self, genre: Genre):
        self._genres.append(genre)

    def get_genres(self) -> List[Genre]:
        return self._genres

    def add_review(self, review: Review):
        super().add_review(review)
        self._reviews.append(review)

    def get_reviews(self) -> List[Review]:
        return self._reviews

    def get_director(self) -> List[Director]:
        return self._directors

    def get_actors(self) -> List[Actor]:
        return self._actors

    # Helper method to return movie index.
    def movie_index(self, movie: Movie):
        index = bisect_left(self._movies, movie)
        if index != len(self._movies) and self._movies[index].release_year == movie.release_year:
            return index
        raise ValueError


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_movies_and_infos(data_path: str, repo: MemoryRepository):
    for row in read_csv_file(os.path.join(data_path, 'Data1000Movies.csv')):
        movie = Movie(row[1], int(row[6]))
        movie.add_id(int(row[0]))
        movie.description = row[3]

        movie.set_director(Director(row[4]))

        genre_lst = row[2].split(",")
        for genre in genre_lst:
            movie.add_genre(Genre(genre.strip()))

        actors_lst = row[5].split(",")
        for actor in actors_lst:
            movie.add_actor(Actor(actor.strip()))

        # Add the movie to the repository.
        repo.add_movie(movie)


def populate(data_path: str, repo: MemoryRepository):
    # Load articles and tags into the repository.
    load_movies_and_infos(data_path, repo)
