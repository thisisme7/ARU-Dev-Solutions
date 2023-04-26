##########################
# ARU Dev Solutions LLC.
##########################

from flask import Flask, render_template, redirect, url_for, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from talisman import Talisman
import threading, hashlib
from flask_login import LoginManager, UserMixin, login_required, login_user

app = Flask(__name__)
engine = create_engine("mariadb+pymysql://root:thisisme@127.0.0.1:3306/arudevsol")
base = declarative_base()
app.config['SECRET_KEY'] = 'secret_key'

Talisman(app)

Session = sessionmaker(bind=engine)
session = Session()

login_obj = LoginManager(app)
login_obj.init_app(app)

class Users(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False)
    password = Column(String(100), nullable=False)

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

class RegisterForm(FlaskForm):
    new_username = StringField('New username', validators=[DataRequired(20)])
    new_password = PasswordField('New passord', validators=[DataRequired(100)])
    submit = SubmitField('Submit')    

class Admin(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

class LoginForm(FlaskForm):
    username = StringField('Username:')
    password = PasswordField('Password:')
    submit = SubmitField('Login')

@login_obj.user_loader
def load_user(username):
        return Admin(username)

@app.route("/", methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        record = session.query(Users).filter_by(username=username).first()
        if username is not None and (record.password == hashlib.sha256(password.encode()).hexdigest()):
            admin = Admin(username)
            login_user(admin)
            return redirect(url_for('admin'))
    return render_template('index.html', form=form)

@app.route("/admin", methods=['POST', 'GET'])
@login_required
def admin():
    form = RegisterForm()
    listofusers = session.query(Users).all()
    if request.method == 'POST' and form.validate_on_submit():
        session.add(Users(id=None, 
                          username=form.new_username.data, 
                          password=form.new_password.data))
        session.commit()
        return render_template("admin.html", 
                               username=None, 
                               password=None, 
                               form=form, 
                               result='User created')
    return render_template("admin.html", 
                            form=form, result="", 
                            listofusers=listofusers)

def http():    
    app.run(host="192.168.10.20", port=80)

def https():
    app.run(host="192.168.10.20", port=443, ssl_context=('cert.pem', 'key.pem'))

if __name__ == '__main__':
    threading.Thread(target=http).start()
    threading.Thread(target=https).start()