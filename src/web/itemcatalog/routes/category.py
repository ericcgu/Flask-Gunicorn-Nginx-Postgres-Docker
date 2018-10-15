from flask import Blueprint, render_template
from itemcatalog.models.category import Category


category = Blueprint('category', __name__)


@category.route('/category/<int:category_id>/')
def items_by_category(category_id):
    """Returns items, category for a specific category"""
    filtered_categories = Category.query.filter_by(id=category_id)
    category = filtered_categories[0]
    return render_template('main.html', title=category.name,
                           categories=filtered_categories,
                           items=category.items)
