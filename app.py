from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)