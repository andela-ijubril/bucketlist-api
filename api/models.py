from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from flask_sqlalchemy import SQLAlchemy
# from .helpers import args_from_url
from .errors import ValidationError

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    # date_created = db.Column(db.DateTime, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self, ):
        db.session.add(self)
        db.session.commit()


class Bucketlist(Base):

    __tablename__ = 'bucketlists'

    name = db.Column(db.String(100), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship("Item", backref='bucketlists', lazy='dynamic')

    def get_url(self):
        return url_for('api.create_bucketlist', created_by=self.created_by, _external=True)

    def to_json(self, with_items=False):
        """ returns a json-style dictionary representation of the bucketlist
            and it's associated items.
        """
        json_bucketlist = {
            'id': self.id,
            'name': self.name,
            'item_count': self.items.count(),
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'created_by': {
                'username': str(self.created_by)
                # 'url': url_for('api.get_user', id=self.created_by, _external=True),
            }
            # 'url': url_for('api.get_bucketlist', id=self.id, _external=True),
        }
        return json_bucketlist

    def delete(self):
        db.session.delete(self)
        db.session.commit()
#
#     def export_data(self):
#         return {'self_url': self.get_url(),
#                 'student_url': url_for('api.get_student', id=self.student_id,
#                                        _external=True),
#                 'class_url': url_for('api.get_class', id=self.class_id,
#                                      _external=True),
#                 'timestamp': self.timestamp.isoformat() + 'Z'}
#
#     def import_data(self, data):
#         try:
#             student_id = args_from_url(data['student_url'],
#                                        'api.get_student')['id']
#             self.student = Student.query.get_or_404(student_id)
#         except (KeyError, NotFound):
#             raise ValidationError('Invalid student URL')
#         try:
#             class_id = args_from_url(data['class_url'], 'api.get_class')['id']
#             self.class_ = Class.query.get_or_404(class_id)
#         except (KeyError, NotFound):
#             raise ValidationError('Invalid class URL')
#         return self


class Item(Base):
    __tablename__ = 'items'

    name = db.Column(db.String(100), index=True)
    done = db.Column(db.Boolean(), default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def to_json(self, with_items=False):
        """ returns a json-style dictionary representation of the bucketlist
            and it's associated items.
        """
        json_bucketlist = {
            'id': self.id,
            'name': self.name,
            'item_count': self.items.count(),
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'created_by': {
                'username': str(self.created_by)
                # 'url': url_for('api.get_user', id=self.created_by, _external=True),
            }
            # 'url': url_for('api.get_bucketlist', id=self.id, _external=True),
        }
        return json_bucketlist
#
#     def get_url(self):
#         return url_for('api.get_student', id=self.id, _external=True)
#
#     def export_data(self):
#         return {'self_url': self.get_url(),
#                 'name': self.name,
#                 'registrations_url': url_for('api.get_student_registrations',
#                                              id=self.id, _external=True)}
#
#     def import_data(self, data):
#         try:
#             self.name = data['name']
#         except KeyError as e:
#             raise ValidationError('Invalid student: missing ' + e.args[0])
#         return self


class User(Base):

    __tablename__ = 'users'

    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128))
    bucketlists = db.relationship("Bucketlist")

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    def export_data(self):
        return {'name': self.name}

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

