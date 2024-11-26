from flask import Flask, render_template

app = Flask(__name__)



@app.route('/')
def home():
    return render_template("index.html")


@app.route('/hello')
def hello_world():
    return "<h1>Hello world!</h1>"