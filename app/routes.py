from datetime import datetime, timezone
from flask import render_template, flash, redirect, url_for, get_flashed_messages, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Post

# MOCK OBJECTS

# user = {
#     "username": "livlyf"
# }

# posts = [
#     {
#         "title": "First Post",
#         "content": "This is the content of the first post.\nIt has two lines."
#     },
#     {
#         "title": "Second Post",
#         "content": "This is the content of the second post.\nIt also has two lines."
#     },
#     {
#         "title": "Third Post",
#         "content": "This is the content of the third post.\nIt has two lines as well."
#     }
# ]

########

@app.context_processor
def inject_user():
    return {'current_user': current_user}

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()



####### main routes
@app.route('/')
@login_required
def home():
    stmt = sa.select(Post).order_by(sa.desc(Post.timestamp)).limit(5)
    latest_five_posts = db.session.scalars(stmt)

    return render_template("home.html", latest_five_posts=latest_five_posts,
                           get_flashed_messages=get_flashed_messages)


@app.route('/login', methods=['GET', 'POST'])
def login():

    # current user is read from the user_loader callback
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(
            User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next = request.args.get('next')
        if not next or urlsplit(next).netloc != '':     # return to home if next param is none or it is directing to a different domain(not we want)
            return redirect(url_for('home'))
        return redirect(next)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congrats! you are now registered")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# profile route
@app.route('/profile/<username>')
@login_required
def profile(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('profile.html', user=user, posts=posts)


# custom error pages
@app.errorhandler(404)
def page_not_found(err):    # type of error is ""werkzeug.exceptions.NotFound""
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(err):
    return render_template("500.html"), 500