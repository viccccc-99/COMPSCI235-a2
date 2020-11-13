from watch_movies.adapters.repository import AbstractRepository
from watch_movies.domain.model import Movie, Review, Actor, Director, Genre


def search_exists(search, select, repo: AbstractRepository):
    genres = repo.get_genres()
    actors = repo.get_actors()
    directors = repo.get_director()
    if select == "Genre":
        if Genre(search) in genres:
            return True
        else:
            return False
    elif select == "Actor":
        if Actor(search) in actors:
            return True
        else:
            return False
    elif select == "Director":
        if Director(search) in directors:
            return True
        else:
            return False