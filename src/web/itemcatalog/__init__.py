import config  # noqa:E401
from faker import Faker
from flask import Flask
from flask_login import LoginManager
from flask import request, render_template
import os

app = Flask(__name__)

# Environment Configuration
app.config.from_object('config.settings.' + os.environ['ENV'])

# User Session Management
login_manager = LoginManager(app)

# Database
from .models import db, user, category, item, ma # noqa:E401
db.create_all()
db.session.commit()

# Seed Users and Categories in Database
if app.config['TESTING'] is True:
    fake = Faker()

    for _ in range(5):
        user.User.seed(fake)

    for _ in range(70):
        category.Category.seed(fake)

@app.route('/', methods=['GET', 'POST'])
def index():
   
    return '/tefff/'


if __name__ == '__main__':
    app.run()