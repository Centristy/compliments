# First, create a ***User*** model for SQLAlchemy. Put this in a ***models.py*** file.

# It should have the following columns:

# - ***username*** - a unique primary key that is no longer than 20 characters.
# - ***password*** - a not-nullable column that is text
# - ***email*** - a not-nullable column that is unique and no longer than 50 characters.
# - ***first_name*** - a not-nullable column that is no longer than 30 characters.
# - ***last_name*** - a not-nullable column that is no longer than 30 characters.

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'


    username = db.Column(db.Text(20), nullable=False, unique=True, primary_key =True,)
    password = db.Column( db.Text, nullable=False)
    email = db.Column(db.Text(50), nullable=False, unique=True,)
    first_name = db.Column(db.Text(30), nullable=False)
    last_name = db.Column(db.Text(30), nullable=False)

    @classmethod
    def signup(cls, username, password, email, first_name, last_name):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name
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
    
    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"
    
    
    

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
