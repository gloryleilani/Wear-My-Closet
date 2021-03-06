"""Models for Wear my Closet app"""

from flask_sqlalchemy import SQLAlchemy 

from datetime import date

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    city = db.Column(db.String)
    phone = db.Column(db.String)
    community_member_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Category(db.Model):
    """A category to organize items by"""

    __tablename__ = 'categories'

    category_name = db.Column(db.String, primary_key=True, unique=True)

    def __repr__(self):
        return f'<Category category_name={self.category_name}>'

class Item(db.Model):
    """An item in a user's closet"""

    __tablename__ = 'items'

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    item_name = db.Column(db.String)
    item_description = db.Column(db.String)
    image_url = db.Column(db.String)
    category_name = db.Column(db.String, db.ForeignKey('categories.category_name'))
    status_code = db.Column(db.String, db.ForeignKey('statuses.checkout_status'), default="Available")
        
    user = db.relationship('User', backref='items')
    category = db.relationship('Category', backref='items')
    status = db.relationship('Status', backref='items')

    def __repr__(self):
        return f'<Item item_id={self.item_id} user_id={self.user_id} name={self.item_name}>'

class Checkout(db.Model):
    """A checkout for a user to borrow items"""

    __tablename__ = 'checkouts'

    checkout_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_borrowed_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    checkout_date = db.Column(db.Date, default=date.today())

    user = db.relationship('User', backref='checkouts')

    def __repr__(self):
        return f'<Checkout checkout_id={self.checkout_id} user_id={self.user_borrowed_by}>'

class CheckoutItem(db.Model):

    __tablename__ = 'checkout-items'

    checkout_item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    checkout_id = db.Column(db.Integer, db.ForeignKey('checkouts.checkout_id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'))
    due_date = db.Column(db.Date)

    item = db.relationship('Item', backref='checkout-items')
    checkout = db.relationship('Checkout', backref='checkout-items')

    def __repr__(self):
        return f'<CheckoutItem checkout_id={self.checkout_id} item_id={self.item_id}>'


class Cart(db.Model):

    __tablename__ = 'carts'

    cart_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    item = db.relationship('Item', backref='carts')
    user = db.relationship('User', backref='carts')

    def __repr__(self):
        return f'<Cart cart_id={self.cart_id} user_id={self.user_id} item={self.item_id}'

class Status(db.Model):
    """The status of an item out for checkout"""

    __tablename__ = 'statuses'

    checkout_status = db.Column(db.String, primary_key=True, unique=True)

    def __repr__(self):
        return f'<Status checkout_status={self.checkout_status}>'

class Community(db.Model):
    """Community page that users can join"""

    __tablename__ = 'communities'

    community_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    community_name = db.Column(db.String)
    community_description = db.Column(db.String)
    members = db.relationship('User', secondary='community_members', backref='communities')

    def __repr__(self):
        return f'<Community community_id={self.community_id} name={self.community_name}>'

class CommunityMember(db.Model):
    """Identifies what community a user is in"""

    __tablename__ = 'community_members'

    community_member_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.community_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    community = db.relationship('Community', backref='community_members')
    user = db.relationship('User', backref='community_members')

    def __repr__(self):
        return f'<Community Member member_id={self.community_member_id} user_id={self.user_id}>'

def connect_to_db(flask_app, db_uri='postgresql:///closets', echo=False):
    """connect to database"""

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

if __name__ == '__main__':
    from server import app

    connect_to_db(app)
