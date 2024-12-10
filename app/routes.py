from flask import render_template, flash, redirect, url_for, get_flashed_messages
from app import app
from app.forms import LoginForm

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
    return render_template("home.html", title="home",
                           user=user, posts=posts,
                           get_flashed_messages=get_flashed_messages)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("login requested for user {}, remember me {}".format(
            form.username.data, form.remember_me.data
        ))
        return redirect(url_for('home'))
    return render_template('login.html', form=form, title="Login")



# custom error pages
@app.errorhandler(404)
def page_not_found(err):    # type of error is ""werkzeug.exceptions.NotFound""
    return render_template("404.html", title="Not Found"), 404

@app.errorhandler(500)
def internal_server_error(err):
    return render_template("500.html", title="Internal Server Error"), 500
