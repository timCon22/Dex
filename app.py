from crypt import methods
from email import header
import json
import os
import pdb
from re import U
from unittest import result
from django.shortcuts import render

from flask import Flask, render_template, flash, redirect, request, session, g
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm
from models import saved_pokemon, user_pokemon, db, connect_db, User

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///pokemon'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

db.init_app(app)

connect_db(app)

#################################################################
# USER/SIGNUP ROUTES
#################################################################


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/')
def homepage():
    """Show homepage"""

    result = []

    if g.user:

        mypokemon = user_pokemon.query.filter_by(user_id = g.user.id).all()
        
        for item in mypokemon:

            current_item = {"poke_id": item.id,
             "pokemon_name": item.pokemon.pokemon_name,
             "pokemon_img": item.pokemon.pokemon_image_url
             }
            print(current_item)
            result.append(current_item)


        return render_template('user/home.html', result=result)
        
    else:
        return render_template('home-anon.html')

# Route for new user to signup

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present fdiorm.
    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                birthday=form.birthday.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('user/signup.html', form=form)

        session["username"] = form.username.data

        do_login(user)

        return redirect("/")

    else:
        return render_template('user/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            form.username.data,
            form.password.data
        )

        if user:
            do_login(user)
            flash(f"Hello, {user.username}! success")
            session["username"] = form.username.data
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('user/login.html', form=form)


@app.route("/signout")
def signout():
    """Logout the user"""
    
    if g.user:
        do_logout()
        session["username"] = None
        return redirect('/')
    else:
        return redirect('/')
    

#################################################################
# POKEMON ROUTES
#################################################################


@app.route('/removePkmn', methods=["GET", "POST", "DELETE"])
def remPkmn():

    poke_id = int(request.form["index"])

    print("poke_id = ", poke_id)

    mypokemon = user_pokemon.query.filter_by(user_id = g.user.id, id=poke_id).delete()

    db.session.commit()

    print(mypokemon)


    return redirect('/')


@app.route('/addPkmn', methods=['POST'])
def addPkmn():
    
    newpokemon = session["pokemon_name"]
    newimg = session["pokemon_image_url"]

    user = g.user.id
    
    exists = saved_pokemon.query.filter_by(pokemon_name = newpokemon).first() 

    if exists == None:
        
        saved_pokemon.add_pkmn_db(
            newpokemon,
            newimg
        )
        
    else:
        pass

    pokemon = saved_pokemon.query.filter_by(pokemon_name = newpokemon).first()

    user_pokemon.save_user_and_pokemon(user, pokemon.id)

    session["pokemon_id"] = pokemon.id

    return redirect('/searchPkmn')


@app.route('/grabPkmn', methods=['POST'])
def grab():

    output = request.get_json()

    serialized_output = json.loads(output)

    session["pokemon_name"] = serialized_output["getPkmn"]["data"]["name"]

    session["pokemon_image_url"] = serialized_output["getPkmn"]["data"]["sprites"]["front_default"]

    return serialized_output


@app.route('/searchPkmn')
def search():

    if g.user:
        return render_template('search.html')
    else:
        return redirect('/')