import datetime
from project import db, bcrypt

class User(db.Model):

    FollowedFollowers = db.Table('followed_followers',
        db.Column('id',
            db.Integer, primary_key=True),
        db.Column('followed_id',
            db.Integer, db.ForeignKey('users.id', ondelete='cascade')),
        db.Column('follower_id',
            db.Integer, db.ForeignKey('users.id', ondelete='cascade')))
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)
    warbles = db.relationship('Warble', 
                              cascade='all, delete-orphan', 
                              backref='user', lazy='dynamic')
    followers = db.relationship('User', 
                                secondary=FollowedFollowers,
                                primaryjoin=(FollowedFollowers.c.follower_id == id),
                                secondaryjoin=(FollowedFollowers.c.followed_id == id),
                                backref=db.backref('following', lazy='dynamic'))

    def __init__(self, username, password, first_name, last_name, email):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return "User {} {}'s user name is {}, email is {}".format(self.first_name, self.last_name,
                                                        self.username, self.email)

class Warble(db.Model):

    __tablename__ = 'warbles'

    id = db.Column(db.Integer, primary_key=True)
    warble = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    def __init__(self, warble, user_id):
        self.warble = warble
        self.user_id = user_id
        self.date = datetime.datetime.today()

    def __repr__(self):
        return "User ID {}'s message: {} at {}".format(self.user_id, self.warble,
                                                      self.date)
