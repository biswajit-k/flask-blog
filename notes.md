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
    * 



read about preflight request and read this - 