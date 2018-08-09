from flask import Flask,render_template,url_for,flash, redirect
from flask_blog import app,db,bcrypt
from flask_blog.forms import RegistrationForm, LoginForm

from flask_blog.models import User,Post
from flask_login import login_user, current_user, logout_user, login_required


posts = [
{
	"author": "Sumedh D",
	"title":"Post 1 ",
	"content":"First port",
	"date":"April 20 2018",

},

{
	"author": "SD",
	"title":"Post 2 ",
	"content":"Second port",
	"date":"April 25 2018"

}


]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",postss=posts)
    #this postss variable will be accessed in html templates to get data from posts list

@app.route("/about")
def about():
    return render_template("about.html", title = "About ")

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_1 =User(username=form.username.data, email=form.email.data, password =hash_pwd)
        db.session.add(user_1) 
        db.session.commit()

        flash(f'Your Account created for {form.username.data}!', 'success')
        # 'success' message here is falls in type category
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


'''
@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

    	if form.email.data == 'admin@blog.com' and form.password.data == 'password':

        	flash('You have been logged in!', 'success')
        	return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            # here there is new category 'danger'
        
    return render_template('login.html', title='Login', form=form)
'''

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            #next_page = request.args.get('next')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
## page will not be accessed it logged out
def account():
    return render_template('account.html', title='Account')

