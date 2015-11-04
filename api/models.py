from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from flask_sqlalchemy import SQLAlchemy

from .errors import ValidationError

db = SQLAlchemy()


class Base(db.Model):
    """
    The base model that every other models in our application inherits from
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()


class Bucketlist(Base):
    """
    Our Bucketlist model that corresponds to bucketlists table
    """

    __tablename__ = 'bucketlists'

    name = db.Column(db.String(100), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship("Item", backref='bucketlists', lazy='dynamic')

    def to_json(self, with_items=False):
        """ put in json format
        """
        json_bucketlist = {
            'id': self.id,
            'name': self.name,
            'item_count': self.items.count(),
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'created_by': {
                'username': str(self.created_by)

            }
        }
        return json_bucketlist

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Item(Base):
    """
    Our Item model that corresponds to items table
    """

    __tablename__ = 'items'

    name = db.Column(db.String(100), index=True)
    done = db.Column(db.Boolean(), default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def to_json(self):
        """ put in json format
        """
        json_bucketlist = {
            'id': self.id,
            'name': self.name,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'url': url_for('api.get_bucketlist', id=self.id, _external=True),
        }
        return json_bucketlist

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(Base):
    """
    Our User model that corresponds to users table
    """

    __tablename__ = 'users'

    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128))
    bucketlists = db.relationship("Bucketlist")

    def hash_password(self, password):
        """
        generate the hash of the password of the user
        :param password:
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        """
        Generate the authenticaton token and it is valid for 3600 seconds
        :param expires_in:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        """
        Verify the token to be use for the current request
        :param token:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

