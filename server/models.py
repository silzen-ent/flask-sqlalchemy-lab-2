from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add a relationship named reviews that establishes a relationship with the Review model. Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Review.
    reviews = db.relationship('Review', back_populates='customer')

    # Update Customer to add an association proxy named items to get a list of items through the customer's reviews relationship.
    items = association_proxy('reviews', 'item',
                                creator=lambda item_obj: Review(item=item_obj))

    # Add serialization rules to avoid errors involving recursion depth (be careful about tuple commas)
    serialize_rules = ('-reviews.customer',)

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    
    # Add a relationship named reviews that establishes a relationship with the Review model. Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Review.
    reviews = db.relationship('Review', back_populates='item')


    # Add serialization rules to avoid errors involving recursion depth (be careful about tuple commas)
    serialize_rules = ('-reviews.item',)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'


class Review(db.Model, SerializerMixin):  # Create a class named Review that inherits from db.Model
    __tablename__ = 'reviews' # a string named __tablename__ assigned to the value 'reviews'.

    id = db.Column(db.Integer, primary_key=True) # an integer column named id that is the primary key.
    comment = db.Column(db.String) # a string column named comment.
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id')) # an integer column named customer_id that is a foreign key to the id column of the customers table.
    item_id = db.Column(db.Integer, db.ForeignKey('items.id')) # an integer column named item_id that is a foreign key to the id column of the items table.

    # a relationship named customer that establishes a relationship with the Customer model. Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Customer.
    customer = db.relationship('Customer', back_populates='reviews')

    # a relationship named item that establishes a relationship with the Item model. Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Item.
    item = db.relationship('Item', back_populates='reviews')

    # Add serialization rules to avoid errors involving recursion depth (be careful about tuple commas)
    serialize_rules = ('-customer.reviews', '-item.reviews')

    def __repr__(self): # a __repr__ method that returns a string representation of the Review instance.
        return f'<Review {self.id}, {self.comment}, {self.customer_id}, {self.item_id}>'
    


## Currently on this step: 
    ## Edit the Customer model to add the following: