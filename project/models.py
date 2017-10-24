import datetime
from project import db, bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)
    warbles = db.relationship('Warble', cascade="all, delete-orphan", backref='user', lazy='dynamic')

    def __init__(self, username, password, first_name, last_name, email):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return "User {} {}'s user name is {}, email is {}".format(self.first_name, self.last_name,
                                                        self.username, self.email)

    # class method to invoke using User.authenticate()    
    @classmethod
    def authenticate(cls, username, password):
        found_user = cls.query.filter_by(username=username).first()
        if found_user:
            authenticated_user = bcrypt.check_password_hash(found_user.password, password)
            if authenticated_user:
                return found_user # return user to store in the session
        return False

class Warble(db.Model):

    __tablename__ = 'warbles'

    id = db.Column(db.Integer, primary_key=True)
    warble = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    def __init__(self, warble, user_id):
        self.warble = warble
        self.user_id = user_id
        self.timestamp = datetime.datetime.today()

    def __repr__(self):
        return "User ID {}'s message: {} at {}".format(self.user_id, self.warble,
                                                      self.timestamp)
