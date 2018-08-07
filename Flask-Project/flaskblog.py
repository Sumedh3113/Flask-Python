from flask import Flask,render_template,url_for,flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '53b73a29a3667dc1ea23f4a484ea'
#dummy data

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        # 'success' message here is falls in type category
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)



@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
    	if form.email.data == 'admin@blog.com' and form.password.data == 'password':
        	flash('You have been logged in!', 'success')
        	return redirect(url_for('home'))
    else:
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
    


if __name__=='__main__':
	app.run(debug=True)