from flask import Blueprint, render_template, jsonify
from itemcatalog.models.category import Category, CategorySchema
from itemcatalog.models.item import Item
from flask_login import current_user


main = Blueprint('main', __name__)


@main.route('/')
@main.route("/home")
def index():
    """Returns all items and categories"""
    categories = Category.query.filter(Category.item_count > 0).order_by(Category.name)  # noqa:501
    items = Item.query.order_by(Item.time_updated.desc())
    return render_template('main.html', title='Home', categories=categories,
                           items=items, current_user=current_user)


@main.route('/api/v1/catalog/json')
def get_catalog():
    """Returns of all categories and nested items in catalog"""
    categories = Category.query.filter(Category.item_count > 0).order_by(Category.name)  # noqa:501
    category_schema = CategorySchema(many=True)
    response = category_schema.dump(categories).data
    return jsonify({'categories': response})
