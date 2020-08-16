"""Server for Wear my Closet app"""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import crud
import api

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "closet"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():

    return render_template('login.html')


@app.route('/mycloset')
def my_closet():

    return render_template('mycloset.html')


@app.route('/mycloset', methods=['POST'])
def upload_image():
    filename = request.files.get('file')
    if filename:
        image_url = api.upload_closet_image(filename)

    return render_template('mycloset.html', image_url=image_url)



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

