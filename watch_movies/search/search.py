from flask import Blueprint
from flask import request, render_template, redirect, url_for, session, flash

from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, Form, StringField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

import watch_movies.adapters.repository as repo
import watch_movies.movie_lib.movie_lib as movie_lib
import watch_movies.search.services as services

search_blueprint = Blueprint(
    'search_bp', __name__)


@search_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    search = MovieSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search.data['search'], search.data['select'])

    return render_template('search/search.html',
                           form=search,
                           title="search",
                           description="search for watch_movies by actor, genre or director")


@search_blueprint.route('/results')
def search_results(search, select):
    search = search.title()
    exists = services.search_exists(search, select, repo.repo_instance)
    if exists:
        if select == "Actor":
            return redirect(url_for('movie_lib_bp.movies_by_actor', actor=search))
        elif select == "Genre":
            return redirect(url_for('movie_lib_bp.movies_by_genre', genre=search))
        elif select == "Director":
            return redirect(url_for('movie_lib_bp.movies_by_director', director=search))
    else:
        flash('No results found!')
        return redirect(url_for('search_bp.search'))


class MovieSearchForm(Form):
    choices = [('Actor', 'Actor'),
               ('Director', 'Director'),
               ('Genre', 'Genre')]
    select = SelectField('search movie:', choices=choices)
    search = StringField('')
