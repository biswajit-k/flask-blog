from flask import render_template
from app import app

# MOCK OBJECTS

user = {
    "username": "livlyf"
}

posts = [
    {
        "title": "First Post",
        "content": "This is the content of the first post.\nIt has two lines."
    },
    {
        "title": "Second Post",
        "content": "This is the content of the second post.\nIt also has two lines."
    },
    {
        "title": "Third Post",
        "content": "This is the content of the third post.\nIt has two lines as well."
    }
]

########

@app.route('/')
def home():
    return render_template("index.html", title="home", user=user, posts=posts)


@app.route('/hello')
def hello_world():
    raise Exception("this raised an exception")
    return "<h1>Hello world!</h1>"


# custom error pages
@app.errorhandler(404)
def page_not_found(err):    # type of error is ""werkzeug.exceptions.NotFound""
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(err):
    return render_template("500.html"), 500
