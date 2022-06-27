from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from housing.logger import logging
from housing.exception import HousingException
import sys

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        raise Exception('Testing exception module...')
    except Exception as e:
        housing = HousingException(e, sys)
        logging.exception('Testing exception module...')
        logging.error(housing.error_message)
    logging.info('Initial Log.')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)