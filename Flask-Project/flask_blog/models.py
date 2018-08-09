from datetime import datetime
from flask_blog import db, login_manager
from flask_login import UserMixin
# For active , anonymous and other users


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    # it refers to other class posts as one user can have many posts
    # backref is used to get the user who created the post
    #lazy attribute is used to get all the posts created by a user
    # here we are referencing the Post class that's why we have Posts

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # datetime.utcnow gives you current time
    content = db.Column(db.Text, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # here we are using Foreign key so referencing table name and column thats why user.id not User.id
    
    #dunder method used for priting the objects
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
