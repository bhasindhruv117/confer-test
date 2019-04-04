from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256 as sha256
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import datetime
template = os.getcwd()+"/web/templates"
app = Flask(__name__,template_folder=template)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'confer-secret-string'

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column('first_name', db.String)
    last_name = db.Column('last_name', db.String)
    email = db.Column('email', db.String)
    password = db.Column('password', db.String)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'id': x.id,
                'first_name': x.first_name,
                'last_name': x.last_name,
                'email': x.email
            }

        return {'users': list(map(lambda x: to_json(x), User.query.all()))}

    @classmethod
    def return_by_id(cls,id):
        def to_json(x):
            return {
                'id': x.id,
                'first_name': x.first_name,
                'last_name': x.last_name,
                'email': x.email
            }
        user = User.query.filter_by(id=id).first()
        if user:
            return to_json(user)
        return None

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @classmethod
    def delete_by_id(cls,id):
        try:
            num_rows_deleted = db.session.query(cls).filter_by(id=id).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

class AuthToken(db.Model):
    __tablename__ = 'authtokens'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column('session_id',db.Integer)
    token = db.Column('token', db.String)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_token(cls, token):
        return cls.query.filter_by(token=token).first()

    @classmethod
    def find_by_session(cls,session_id):
        def to_json(x):
            return {
                'token': x.token
            }

        return {str(session_id): list(map(lambda x: to_json(x), cls.query.filter_by(session_id=session_id).all()))}

    @classmethod
    def send_email(self,session_id,email):
        fromaddr = "conferapp123@gmail.com"
        toaddr = email
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Authentication for Confer Session"
        body = "You have a session {} on confer, kindly use the given QR code to enter in the chat room.".format(session_id)
        msg.attach(MIMEText(body, 'plain'))
        filename = "qr.png"
        attachment = open("qr.png", "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attachment.read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, "confer11")
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()

class PublicDiscussions(db.Model):
    __tablename__ = 'public_discussions'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name',db.String)
    hosted_by = db.Column('hosted_by', db.String)
    date = db.Column('date', db.DateTime)
    created_datetime = db.Column('created_datetime', db.DateTime,default=datetime.datetime.utcnow())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'id': x.id,
                'name' : x.name,
                'hosted_by': x.hosted_by,
                'date': x.date,
                'created_datetime': x.created_datetime
            }

        return {'public_discussions': list(map(lambda x: to_json(x), PublicDiscussions.query.all()))}


