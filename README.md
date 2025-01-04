# Flask Blog Notes

* create a folder `app` and make it a package by adding a `__init__.py` file and add the initial flask code there
* `app = Flask(__name__)` here, __name__ means the package name(if its __init__ file then means folder name, else its the file name(_also called the module_)).

    * this first parameter is important as it tells what belongs to the application

    * the package name will now be used to resolve path to resources, so it finds `static` and `templates` folder relative to the file

    * also other extensions like flask-sqlalchemy will generate debug logs only for files inside the package or files/folders relative to the module(means .py file)


* Before heading to database/fetching logic it is always beneficial to
create mock object that you are expecting and write code using that. Later on
you just have to replace the object with the fetched object from database/api.

For example, we can create a dictionary of a user for mocking. Like `user = {
    "name": "mock user"
}`

* WTForms provides-
    * data validation
    * csrf protection
    * internationalization(i18n)
    
* internationalization(i18n) is done to allow different language support to app
    * For this content is loaded dynamically from language.json file. Also, 
        other data like images, etc are also loaded same way(because image text can also differ)
    * date, content format according to language, also rtl, ltr is done
    * we do it using `x=_("hello")`. Here, `_()` function converts to the locale language. In Django, we import it in `utils.translation`, in Flask we use *Flask-Babel* extension for this function.



## Security notes
* Security issues arise on user's side through cross origin request. If every origin can only access/send request to
their origin, then things are safe.

    However, this means no microservices, no api access and many other restrictions.
    Therefore it is essential to allow Cross origin resource sharing, but in a controlled way.

* Cross origin access for some type of resources is allowed like css, img, script loading, etc with 
restrictions.
* Security of users begins at using browser. Browser apply the above web rules, etc to protect the user.
Had the user been using other ways to access resources like cURL, etc then these security restriction like
blocking other site from reading response, etc won't be applied and user's data is compromised.
* Therefore security rules like same origin policy are only useful if user is accessing site using
their secure browser. 
* for any request that changes user's data, use CSRF token. This ensure that any request originated from
different source is not served. Only request originated from app's UI is considered authentic.

* We at server standpoint should know the security vulnerabilities and practices to mitigate them.
Going through OWASP guide for top security threats and setting system to mitage them is essential.

* Important principle - Any security given in the hands of client is vulnerable.
* Security can only be enhanced, it can never be completely guaranteed. But as a developer be optimistic
and try to implement it atleast till the standard levels. *That's why go through the OWASP to see the baseline
standards.*

* **CSRF attacks**

    * although same origin policy prevents XSS attack, where malicious site can't read data from other site on
    which user is logged in like the session id, DOM, etc. It still doesn't prevent other site to send
    request cross site(like user's bank website) from their site js itself.

    * Even through they won't get the response, but they could trigger some action like sending money
    from user's account to theirs.
    * We can think of ways to mitigate them. The best one is to use **CSRF token**. However, let's
    talk about other ways as well and the possible loophole in them.

    * **alternate 1**

        * At the server, check the origin of request, if different site then block it. But, it is
        possible to alter the origin in the browser as well if we have a malicious extension on browser.
        It could control the request heanders.
        * Also, who prevents you(*as an attacker*) from sending a cURL request with headers of your choice.
        However, in that case you would have to manage getting the user's session id for authenticity.


    * **alternate 2**
        
        * On user's side, they are insecure if their cookies are insecure, because on server I only
        use the cookies to check the authenticity. So, it is very important to secure the cookies.
        * Using the `sameSite=Strict` header while setting the cookie will not send cookie cross-site
        * however, it is [still vulnerable to CSRF](https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions).

    * The **CSRF token** technique

        * The server generates a random strong token and attach it with the use's session(*on server*)
        * It then sends the token along with the form as a input hidden field like-

            `<input type="hidden" name="csrf-token" value="CIwNZNlR4XbisJF39I8yWnWX9wX4WFoz" />`

        * On receiving the response from the user, check if the token value matches.

* **Preflight Request** - This is a HTTP OPTIONS request(like POST, GET, PUT) that the browser sends for
non trivial CORS reqeuests.

    * Before CORS mechanism, cross origin reqeuests were allowed but with restricted content-type
    like plain/text, multipart/formdata, etc. So, servers had to deal with them
    * When CORS was introduced, it allowed content type application/json to be sent to server
        but only if the server allowed. This allow/not allow is done through preflight request.

    * So, the previous type of requests remained without pre-flight, but newer request which were 
    introduced had preflight request.

    * This adds the backward compatibility that old server implementation would keep working normally. 

* The core idea behind Flask is to provide minimal interface and apis to run a server. Flask extensions
are utilities that you can add on top of it. Each extension comes with its own principle(*like 
Flask-restful uses classes to have GET/POST method for a route*)

* use config.py module where you create a `Config` class and put configurations as class members.
If you have different sets of configurations, you can subclass and add there.

## WTForms

* ease in writing forms - provides validation, CSRF protection, less code and more understandable

Below is the core concept behind it-

* We create a class for a form. The form fields are made using, different `Field` classes. Like below-
    ```python
    from wtforms import Form, BooleanField, StringField, validators

    class RegistrationForm(Form):
        username = StringField('Username', [validators.Length(min=4, max=25)])
        email = StringField('Email Address', [validators.Length(min=6, max=35)])
    ```

* Validators are provides inside a list, custom validators can also be created by defining function that takes parameters like `def is_42(form, field): ...`

* Form can also be subclassed, like above `RegistrationForm` can be sub classed into `AdminRegistrationForm` and it would extend the fields of parent Form.

* Each field will internally create its own markup. Like `StringField` will create `<input type="string" ...>`.

* Below is a simple way to use form-

    ```python
    def register(request):
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.save()
        redirect('register')
    return render_response('register.html', form=form)
    ```

    **Steps**
    * create the form class
    * create form object from that class and pass the request body we got in form
        as the constructor.
    * before using form data do `form.validate()` to see if no errors are present
    * if errors are present, they could be seen by `form.errors`. It would give error
    for each field(if present) in a dictionary.
    * use form data by `form.username.data`


    * in constructor we can pass 3 parameters - formdata(*request.POST*), object(*user*),
    and keyword arguments(*name="rajesh"*). Form will first apply everything from formdata, then see fields in object if not already persent apply those then if some
    field from keyword args not present already, apply that. Like below-
    
        ```python
        form = ChangeUsernameForm(request.POST, user, username='silly')
        ```
    * styling and other attributes can be added to resulting HTML tag of field by
    passing inside the `__call__()` function. Like - `form.name(class_="text-red-200", 
    data-extra="abcd")`.

        It would be rendered like-
        `Markup('<input class="text-red-200" id="name" name="name" type="text" 
        data-extra="abcd"')`

    * In template we can use it like-
        ```html
        <form method="POST" action="/login">
            <div>{{ form.username.label }}: {{ form.username(class="css_class") }}</div>
            <div>{{ form.password.label }}: {{ form.password() }}</div>
        </form>
        ```

    * If we also want to display error-

        ```html
        <form method="POST" action="/login">
            <div>{{ form.username.label }}: {{ form.username(class="css_class") }}</div>
            {% if form.username.errors %}
                <ul class="errors">{% for error in form.username.errors %}<li>{{ error }}</li>{% endfor %}</ul>
            {% endif %}

            <div>{{ form.password.label }}: {{ form.password() }}</div>
            {% if form.password.errors %}
                <ul class="errors">{% for error in form.password.errors %}<li>{{ error }}</li>{% endfor %}</ul>
            {% endif %}
        </form>
        ```

    * We could also manually create form like `<input type='...', name='...'>` but
    we need to make sure that mapping of input `name`, `type` matches with the `Field` of
    class

    * Flask-wtf provides additional functionality of CSRF token

---

* In flask, `redirect(*<url>*)` and `url_for(*<route>*)`. So, we can use like - `redirect(url_for('home'))`. we should use `url_for` because URLs are much more likely to change than view function names, which are completely internal

    also use it in html templates like `<a href="{{ url_for('index') }}">Home</a>`

* to return a message for success/failure of some action, we can use flask `flash`. register a message
using `flash()` function and use it once on calling `get_flash_message`

```python
from flask import flash, get_flashed_messages, redirect, url_for

@app.route('/')
def index():
    return render_template('index.html', get_flash_messages=get_flashed_messages)


@app.route('/login')
def login():
    ...
    if login.success():
        flash("login success!")
        return redirect(url_for('index'))
```

and in html,

```html
...
...
        {% with messages = get_flashed_messages() %}
        {% if messages %}
        <ul>
            {% for message in messages %}
            <li>{{ message }}</li>
            {% endfor %}
        </ul>
        {% endif %}
        {% endwith %}
...
...
```

* To create custom validators, create a member function in form like `validate_<field_name>`

* while create your own package, where you have `setup.py` for development, do `pip install -e .` within the package. This will install your package in editable mode(*creates symbolic link to package*)
and when you change anything in your package, it is reflected. Without it, your package is installed
directly in `site-packages` folder and you would have to change code there.

* in python `sys.path` contains list of paths(*str*) where python searches for modules. So, when you
have some module in a uncommon location, you can add it to path so python can find it and you could
easily import. like `sys.path.append(...)` 

## Alembic

* Migration tool for sqlalchemy
* Aim of migration is to automatically lift(*or possibly downgrade*) the database to the recent(*or the given*) version of
what the schema in code represents
* Migration applied to DDL. Which means, table and database creation, its schema
* Generates template for migration
    * a folder inside application gets created called migration environment
    * `env.py` file is created that contains main migration code
    * Then we have a `versions/` folder where all are py script and each
        apply a migration patch(*basically a script that applies new changes on top
        of existing data*)
    * command is - `alembic init <migration-environment-name>`
    * there are templates available for migration environment which we can 
    choose while initializing the env
* general configration of alembic, logging, etc are stored in `alembic.ini`. We can tune it
* Each migration script looks like-
    ```python
        revision = '1975ea83b712'
        down_revision = None        # previous version it will go to on downgrade(linked list type of)
        branch_labels = None

        from alembic import op
        import sqlalchemy as sa

        def upgrade():
            pass        # upgradation codd

        def downgrade():
            pass        # optional but preferred
    ```

* command is - `alembic upgrade head`, head upgrades to latest
version. instead of head, we can provide specific revision_id also.
* when ran for 1st time, a table called `alembic_version` is made which will hold
 current version of db

* **Steps**

    * `alembic init <migration-env-name>`
    * in the `alembic.ini` file change database uri
    * write the model in `models.py` file
    * in `env.py` file correct the import for model with the one you
        created
         ```python
            from myapp.mymodel import Base
            target_metadata = Base.metadata
        ```
    * run `alembic revision --autogenerate -m "create models"`
        * This will create a migration file upon running which we will be
            able to initialize our db with the tables
    * to run the migration script do - `alembic upgrade head`

* **How autogenerate migrations work?**

    Alembic uses database uri present in `alembic.ini` to see current state of database
    and the `Base.metadata` in `env.py` file to see the models of db.
    
    It then generates the "obvious" steps for going from [database state → state of
    models defined in models.py file]

    Alembic doesn't detect table/column name change. It sees it as a drop table/column
    then add a table/column

* There is no need of migration if you want to lift the db from blank schema to the latest version.
SQLAlchemy's `db.create_all()` does it out of the box. The need of Alembic or db migration in general
is to lift/downgrade between versions.

* **When to remove a migration script?**
    * When no database environment is at that version and all have moved to a more recent state.

    * To remove the old migration scripts, delete them, and set the left oldest file `down_version = None`

* **Directive and Event Listeners**
    * Directives are the inbuilt/user-defined functions for common DDL operations for migration work. Like-
        `op.create_table()`, `op.add_column()`, etc.
    * Event listener help calling custom function before/after a event. Like a trigger. For example, `before_indexing` etc.
    * Using directives and hooks we can add modification in our migration logic.

* **Useful when**
    * make migration easy, don't have to manually update db. Just validate the script
    and then call it, without even caring if the server is started/not
    * helps in maintaining versions of db
    * when we have dev. and prod. envs running, and we need to update db table structure, we just need
    to validate the migration script and call it at both dev. and prod.

## Flask-Migrage
* uses alembic for migration. 
* We need to configure our `app.config[db_uri]` and initialize a migrate object
using `migrate = Migrate(app, db)`
* to use flask migrate we need to use `flask db` prefix
* commands
    * `flask db init` - initialize migration folder and env.
    * `flask db migrate` - create migration script for current db model state
    * `flask db upgrage` - calls all scripts in correct order to reach recent state
* Great thing about db migration is that you don't have to run your server for applying changes.
The script takes the db uri and call the changes to be done.

## Flask-sqlalchemy
* `username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)` 

    This way using type hints we do mapping. 
* `timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))`

    In above, default value is a function that returns the now datetime in utc

* **Structuring db model for foreign key**

    * Minimum requirement is - `  user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)`
    * to also add back refrence in both user and posts table.
        * In post table, `author: so.Mapped[User] = so.relationship(back_populates='posts')`
        * in user table, - `posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')`
        * These variables will not be part of db tables. just for use in model and code. Internally they will
        call join and where query.

---
* **application context**
    Flask uses application context to store config/variables at global level
    that can be accessed without the `app` object. This helps in preventing
    circular import issues and is also convinient.

    By default when running app through `flask run` the app context is automatically
    pushed before every request is handled. However, when running from interactive
    shell, we need to explicitly pass it using-

    `>>> app.app_context().push()` or we can also do `flask shell` which automatically
    does this.

    To also load other objects in shell, we need to add below code in our FLASK_APP file-
    ```python        
        @app.shell_context_processor
        def make_shell_context():
            return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}
    ```

## Flask-login

* Provides structure and flexibility in implementing login related functionalities in
flask app
* Basic idea is to ask developer to implement certain classes, functions and variables
which will then be used in login flows

    Like implement some functions in `User` class -
    * `is_authenticated`
    * `is_active`
    * `is_anonymous` 
    * `get_id` 

* ```python
    if not url_has_allowed_host_and_scheme(next, request.host):
        return flask.abort(400)
    ```
    
    Above function is used when redirect is done based on the `next` parameter present in url.
    Like `https://my_website.com/login?next=dashboard`
    
    Here, it is possible that attacker can create malicious link where user is redirected to route
    where a money transfer/details are sent. like `https://my_website.com/login?next=transfer&account=attacker`

    This function implemented by developer checks if host is trusted and the next parameter is fine, then
    proceed, else abort.

* logged in user can be accessed in all html pages like-
    ```python
        {% if current_user.is_authenticated %}
        Hi {{ current_user.name }}!
        {% endif %}
    ```

* routes that require user login can be decorated with `@login_required` like below-
    ```python
    @app.route("/settings")
    @login_required
    def settings():
        pass
    ```
    This will put `/settings` in `next` parameter
     and check if user is logged in, if yes, then redirect it to `next`, else abort. To set
     custom view other than abort, see next point. 

* to set a custom view to which user will be re-directed when they are not logged in is-
`login_manager.login_view = "<route-function-name>"`

* we have a `LoginManager` class provided by flask-login which packs all the login functionality
    To use it, we need to define some callback functions on it. Like-

    * to load user from user_id
        ```python
        @login_manager.user_loader
        def load_user(user_id):
            return User.get(user_id)
        ```
    * to load user from the api_key or auth token, we will use the request object
        ```python
        @login_manager.request_loader
        def load_user_from_request(request):

            # first, try to login using the api_key url arg
            api_key = request.args.get('api_key')
            if api_key:
                user = User.query.filter_by(api_key=api_key).first()
                if user:
                    return user

            # next, try to login using Basic Auth
            api_key = request.headers.get('Authorization')
            if api_key:
                api_key = api_key.replace('Basic ', '', 1)
                try:
                    api_key = base64.b64decode(api_key)
                except TypeError:
                    pass
                user = User.query.filter_by(api_key=api_key).first()
                if user:
                    return user

            # finally, return None if both methods did not login the user
            return None
        ```
    * to modify default behaviour. For example instead of redirecting to login page
    if user is not authorized.

        ```python
        @login_manager.unauthorized_handler
        def unauthorized():
            # do stuff
            return a_response
        ```
* for session cookie protection, flask-login internally stores the hash of (user IP + user agent)
inside the session itself. This helps in ensuring that access happens from the same network(*using IP*)
and also from the same browser/client app(*using user agent*)

    It offers three modes `none`, `basic`(*default*), `strong`

    * `basic` - checks hash on session state change requests(like login/logout). Not much useful
    * `strong` - checks session on every request. Should be used.

        done by - `login_manager.session_protection = "strong"`

* **protected routes**

    * set the login view
    ```python
        login = LoginManager(app)
        login.login_view = 'login'  # set value to function that is used to show login page
    ```

    * define the route with login required
    ```python
        @app.route('/dashboard')
        @login_required             # it will ensure that login user are shown this page, else re-direct to login page first
        def dashboard():
            ...
            ...
    ```

    This also sets the `next` parameter in request like - `/login?next=/dashboard`. This is useful as we will
    check this parameter to redirect the user to dashboard view after login directly.

    * 

---

* to include a jinja component in between-
    ```html
        {% include '_post.html' %}
    ```

    I name underscore to distinguish component templates from pages

* to run a function before each route-
    ```python
        @before_request
        def before_request():
            pass
    ```

* in flask debug mode, the error we see on browser, we can expand any of the stack trace and see
the value of variables inside them

* **error handlers**
    create a `errors.py` file and create custom error pages-
    ```python
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    ```

    * We can send errors to email apart from logging like `from logging.handlers import SMTPHandler`

    * To run a local SMTP server to test email functionality-
        
        * `pip install aiosmtpd`
        * start local server

            `aiosmtpd -n -c aiosmtpd.handlers.Debugging -l localhost:8025`

    * To log to a file-
        
        * `from logging.handlers import RotatingFileHandler`

        * below is code-
            ```python
            if not app.debug:
            # ...

            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                            backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info('Microblog startup')
            ```
        * The RotatingFileHandler class is nice because it rotates the logs, ensuring that the log files do not grow too large when the application runs for a long time. In this case I'm limiting the size of the log file to 10KB, and I'm keeping the last ten log files as backup.

* **database relations**

    * one-to-many is done by foreign key
    * many-to-many is done by creating a extra association table
    * one-to-one is like one-to-many + unique constraing on foreign key

    * to create a table without class model-
        ```python
        followers = sa.Table(
        'followers',
        db.metadata,
        sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'),
                primary_key=True),
        sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'),
                primary_key=True)
        )
        ```
    * Self association table-
        ```python
        class User(UserMixin, db.Model):
        # ...
        following: so.WriteOnlyMapped['User'] = so.relationship(
            secondary=followers, primaryjoin=(followers.c.follower_id == id),
            secondaryjoin=(followers.c.followed_id == id),
            back_populates='followers')
        followers: so.WriteOnlyMapped['User'] = so.relationship(
            secondary=followers, primaryjoin=(followers.c.followed_id == id),
            secondaryjoin=(followers.c.follower_id == id),
            back_populates='following')
        ```

        We can add/remove follower of a user by `user1.following.add(user2)`, `user1.following.remove(user2)`

* separating business logic from view functions to model functions **makes unit testing easier**. Like, we can
create a function inside `User` model to add/remove follower instead of directly calling `user.following.add(...)`

## Misc

* In SQLalchemy Declarative Base contains metadata (`Base.metadata`), 
which holds all the table and schema information for the ORM. 
This metadata can be used to create or 
manage the database schema programmatically.

* SQLite don't provide full `ALTER` functionality
    * it don't provide command for dropping column, changing its dtype, etc

    * The way to do it is to create new table, copy content there and drop old one

* md5 takes a byte type and hashes it. Below are two ways to convert string to byte-

    ```python
        b_hello = b'hello'  # ascii encoding
        bb_hello = 'hello'.encode('utf-8')  # UTF-8 encoding
    ```

    ascii encoding can encode 128 character types, special characters can't be encoded in this scheme.
    Here, UTF-8 encoding would be required