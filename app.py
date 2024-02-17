from flask import Flask,request,render_template,redirect, url_for,flash,session
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from wtforms import Form,IntegerField,BooleanField,TextAreaField,validators,StringField,DecimalField,PasswordField
from wtforms import Form, StringField, TextAreaField, PasswordField,SubmitField,validators, ValidationError,IntegerField

currentlocation=os.path.dirname(os.path.abspath(__file__))
myapp=Flask(__name__)
brcypt=Bcrypt(myapp)
myapp.config['SECRET_KEY']='ufhujhguirur7474397344947479'
myapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///final_ffdbjjhdfe3hhd2.db'
db=SQLAlchemy(myapp)
#User model
class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False) 
    phone = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
db.create_all()


@myapp.route('/chatbot')
def chatbot():
    return render_template('ChatBot.html')

#since there are only one form that also takes data from one model
#no need to split it
#form for login
class Login_Form(Form):
    email = StringField('', [validators.Email(), validators.DataRequired()])
    password = PasswordField('', [validators.DataRequired()])

#user registerform
class Register_form(Form):
    name = StringField('Name: ',[validators.DataRequired()])
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])
    phone=IntegerField('Phone No.(Include STD code)',[validators.DataRequired()])
    submit = SubmitField('Register')
    #validation
    def validate_username(self, username):
        if Users.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")
        
    def validate_email(self, email):
        if Users.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")



def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

@myapp.route('/')
def home():
    if 'username' in session:
        login=True
    return render_template('index.html')

@myapp.route('/Meditation')
def Meditation():
    return render_template('Meditation.html')
@myapp.route('/AskHelp')
def AskHelp():
    return render_template('askhelp.html')

@myapp.route('/register',methods=['GET','POST'])

def register():
    form=Register_form(request.form)
    if request.method=='POST' and form.validate():
        try:
            hash_password=brcypt.generate_password_hash(form.password.data).decode('utf-8')
            user=Users(name=form.name.data,username=form.username.data,password=hash_password,email=form.email.data,phone=form.phone.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Welcome {form.username.data} Thanks for registering.Please proceed with login','success')
            return redirect(url_for('login'))
          
        except Exception as e:
            flash('Something went wrong','danger')
            
    return  render_template('signin.html',form=form,title='registration pages')


@myapp.route('/login',methods=['GET','POST'])
def login():
    form=Login_Form(request.form)
    if request.method=='POST':
        user=Users.query.filter_by(email=form.email.data).first()
        if user and brcypt.check_password_hash(user.password,form.password.data):
            session['email']=form.email.data
            session.permanent=True
            flash(f'Welcome {form.email.data}','success')
            return render_template('index.html')
        else:
            flash('Incorrect credentials,please check your credentials or signup to login!','danger')
    return render_template('login.html',form=form,title='Login')




















'''
@myapp.route('/register',methods=['GET','POST'])

def registerpage():
    form=Register(request.form)
    if request.method=='POST' and form.validate():
        try:
            hash_password=brcypt.generate_password_hash(form.password.data).decode('utf-8')
            user=Users(username=form.username.data,password=hash_password,email=form.email.data,phone=form.phone.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Welcome {form.username.data} Thanks for registering.Please proceed with login','success')
            return redirect(url_for('login'))
          
        except Exception:
            flash(f"email already exists",'danger')
            
    return  render_template('signin.html',form=form,title='registration pages')

@myapp.route("/login",methods=['GET','POST'])
def login():
    form=Login(request.form)
    if request.method=='POST':
        user=Users.query.filter_by(email=form.email.data).first()
        if user and brcypt.check_password_hash(user.password,form.password.data):
            session['email']=form.email.data
            session.permanent=True
            flash(f'Welcome {form.email.data}','success')
            return url_for('index')
        else:
            flash('Incorrect credentials,please check your credentials or signup to login!','danger')
            return redirect('register')
    return render_template('login.html',form=form,title='Login')
'''

if __name__=="__main__":
    myapp.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    myapp.run(host='0.0.0.0', port=port)



