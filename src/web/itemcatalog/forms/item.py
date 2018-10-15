from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from itemcatalog.models.category import Category


def all_categories():
    return Category.query.order_by(Category.name.asc())


class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = QuerySelectField(u'Category',
                                get_label=u"name",
                                query_factory=all_categories,
                                allow_blank=False)
    submit = SubmitField('Post')
