from . import db, ma
from .item import Item, ItemSchema
from datetime import datetime
from marshmallow import fields
from sqlalchemy import exc, select, func
from sqlalchemy.ext.hybrid import hybrid_property


class Category(db.Model):
    """Model to define Category"""
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False, unique=True)
    items = db.relationship('Item', backref='category', lazy='joined')
    time_inserted = db.Column(db.DateTime(), default=datetime.utcnow)
    time_updated = db.Column(db.DateTime(), default=datetime.utcnow)

    @hybrid_property
    def item_count(self):
        """hybrid attribute has distinct class and instance level behavior"""
        return len(self.items)

    @item_count.expression
    def item_count(cls):
        """hybrid attribute has distinct class and instance level behavior"""
        return (select([func.count(Item.id)])
                .where(Item.category_id == cls.id)
                .label("item_count"))

    @classmethod
    def seed(cls, fake):
        """class utility to create fake accounts to see the db"""
        category = Category(
            name=fake.state()
        )
        category.save()

    def save(self):
        """persists obj to db"""
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()


class CategorySchema(ma.ModelSchema):
    """Define marshmallow schema"""
    class Meta:
        """Define marshmallow schema"""
        model = Category
    items = fields.Nested(ItemSchema, many=True,
                          only=['id', 'name', 'description',
                                'time_inserted', 'time_updated'])
