"""SQLAlchemy models for Capstone."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import pdb

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.Text,
        nullable=False
    )

    user_saved_pokemon = db.relationship("user_pokemon", backref='users_saved_pokemon')
    
    birthday = db.Column(
        db.Text
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"


    @classmethod
    def signup(cls, username, email, password, birthday):
        """Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            email=email,
            birthday=birthday
        )

        db.session.add(user)
        return user


    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class user_pokemon(db.Model):

    __tablename__ = "user_pokemon"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    pokemon_id = db.Column(
        db.Integer,
        db.ForeignKey('saved_pokemon.id', ondelete='cascade')
    )

    pokemon = relationship("saved_pokemon", backref="user_pokemons")

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    def save_user_and_pokemon(user, pokemon):
        result = user_pokemon(
            pokemon_id=pokemon,
            user_id=user
        )

        db.session.add(result)
        db.session.commit()
        return



#################################################################
# POKEMON DB MODELS
#################################################################


class saved_pokemon(db.Model):

    __tablename__ = "saved_pokemon"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    pokemon_name = db.Column(
        db.Text,
        nullable=False
    )

    pokemon_image_url = db.Column(
        db.Text,
        nullable=False
    )

    @classmethod
    def add_pkmn_db(cls, name, image):
        pkmn = saved_pokemon(
            pokemon_name=name,
            pokemon_image_url=image
        )

        db.session.add(pkmn)
        db.session.commit()
        return pkmn

##############################################################################



def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)