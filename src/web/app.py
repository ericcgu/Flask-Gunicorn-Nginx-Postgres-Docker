from flask import Flask
from flask import request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
   
    return '/tefff/'


if __name__ == '__main__':
    app.run()
