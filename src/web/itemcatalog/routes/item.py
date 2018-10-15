from flask import (render_template, url_for, request,
                   redirect, Blueprint, abort, flash)
from flask_login import current_user, login_required
from itemcatalog import db
from itemcatalog.models.item import Item
from itemcatalog.forms.item import ItemForm
from sqlalchemy import func

item = Blueprint('item', __name__)


@item.route("/item/create", methods=['GET', 'POST'])
@login_required
def create_item():
    """CREATE Item"""
    form = ItemForm()
    if form.validate_on_submit():
        new_item = Item(name=form.name.data,
                        description=form.description.data,
                        category=form.category.data,
                        user=current_user)
        db.session.add(new_item)
        db.session.commit()
        flash('Your job listing has been successfully created!', 'success')
        return redirect(url_for('main.index'))
    return render_template('item.html', form=form)


@item.route("/item/<int:item_id>/update", methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    """
    UPDATE Item
    :param item_id: item_id (int) for Item
    """
    item = Item.query.get_or_404(item_id)
    if item.user != current_user:
        abort(403)
    form = ItemForm()
    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        item.category = form.category.data
        item.time_updated = func.now()
        db.session.commit()
        flash('Your job listing has been successfully updated!', 'success')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.name.data = item.name
        form.description.data = item.description
        form.category.data = item.category
    return render_template('item.html', form=form)


@item.route("/item/<int:item_id>/delete", methods=['POST'])
@login_required
def delete_item(item_id):
    """
    DELETE Item
    :param item_id: item_id (int) for Item
    """
    item = Item.query.get_or_404(item_id)
    if item.user != current_user:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Your job listing has been successfully deleted!', 'success')
    return redirect(url_for('main.index'))
