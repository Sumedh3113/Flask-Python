import os
# os module to save the file with same extension as uploaded 
import secrets
# to generate new name every time you upload the file

from PIL import Image
# for resizing the image

from flask import Flask,render_template,url_for,flash, redirect,request, abort
from flask_blog import app,db,bcrypt, mail
from flask_blog.forms import (RegistrationForm, LoginForm, UpdateAccountForm, PostForm, 
                             RequestResetForm, ResetPasswordForm)

from flask_blog.models import User,Post
from flask_login import login_user, current_user, logout_user, login_required

from flask_mail import Message



@app.route("/")
@app.route("/home")
def home():
    # get page 1 by default and type is int so if someone passes value other than int it will throw an error 
    page = request.args.get('page', 1 , type = int)
    # to grab all the post from database
    #posts = Post.query.all()
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page=2)
    
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
            next_page = request.args.get('next')
            # if we try to access account page without logging in then we will redirected to login page 
            #but after we login we will be redirected to about page directly instead of home page
            return  redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # the function .splittext()  will give file_name and extention
    # since we  dont need file name we use _ , f-ext 
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # here we are saving the uploaded picture at above path but before 
    #form_picture.save(picture_path)
   
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    # i is new form_picture 
    i.save(picture_path)
    
     
    # returning picture file name so that user can use it outside this function
    return picture_fn

@app.route("/account",methods=['GET', 'POST'])
@login_required
## page will not be accessed it logged out
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            # saving the picture from form field
            picture_file = save_picture(form.picture.data)
            # passing image to current user ()image file is a attribute below
            current_user.image_file = picture_file
        # Committing new changes 
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        # here after making changes we are redirecting the page to get an updated response from server
        # i.e we are sending GET request to the server if we reload it using render_temp we will send POST req 
        # which is not good
        return redirect(url_for('account'))
    elif request.method == 'GET':
        #retrieving new changes
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


#for adding the post
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # here we are creating the post
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    # legend is used to pass title of the form same in update post function
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')




@app.route("/post/<int:post_id>")
def post(post_id):
    # fetching post if post is not exist return 404 error
    post = Post.query.get_or_404(post_id)
    # every post has a id and seperate html page will be assigned to it
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # so that the user who wrote the post will be able to update it
    if post.author != current_user:
        # 403 is used for forbidden access
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        # to populate the update form with existing post data 
        post.title = form.title.data
        post.content = form.content.data
        # we dont need to do add as these changes are already in the database we just need to update it
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=2)
    return render_template('user_posts.html', posts=posts, user=user)

# body msg of mail with reset link external is used to get external url not relative url 
# relative url is used for internal link external for full seperate domain

def send_reset_email(user):
    token = user.get_reset_token()
    # subject , sender & receiver of mail
    msg = Message('Password Reset Request',
                  sender='sumedhdeshpande31@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        # this verify method is defined in models.py
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    # this form variable will collect data from the ResetPasswordForm() field
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)