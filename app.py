from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5
from housing.logger import logging
from housing.exception import HousingException
import sys

app = Flask(__name__)
bootstrap = Bootstrap5(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/roadmap', methods=['GET'])
def roadmap():
    return render_template('roadmap.html')

@app.route('/data', methods=['GET'])
def data():
    return render_template('data.html')

@app.route('/eda', methods=['GET'])
def eda():
    return render_template('eda.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=e)

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', e=e)

    
if __name__ == '__main__':
    app.run()