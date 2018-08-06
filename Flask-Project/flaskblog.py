from flask import Flask,render_template,url_for
app = Flask(__name__)

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


if __name__=='__main__':
	app.run(debug=True)