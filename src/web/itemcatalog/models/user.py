from . import db
from datetime import datetime
from itemcatalog import login_manager
from flask_login import UserMixin
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from sqlalchemy import exc


@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id user to retrieve

    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """Model to define User"""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    items = db.relationship('Item', backref='user', lazy=True)
    time_inserted = db.Column(db.DateTime(), default=datetime.utcnow)
    time_updated = db.Column(db.DateTime(), default=datetime.utcnow)

    @classmethod
    def seed(cls, fake):
        """class utility to create fake accounts to see the db"""
        user = User(
            name=fake.name(),
            email=fake.email()
        )
        user.save()

    def save(self):
        """persists obj to db"""
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()


class UserAuth(db.Model, OAuthConsumerMixin):
    """Model to define UserAuth to store oAuth tokens"""
    __tablename__ = 'userauth'

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
