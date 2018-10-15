from itemcatalog import app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
__all__ = ["db", "ma"]

db = SQLAlchemy(app)
ma = Marshmallow(app)
