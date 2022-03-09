from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class MenuModel(db.Model):
    __tablename__ = 'main_menu'

    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    url = db.Column(db.Text())

    def __init__(self, _id, title, url):
        self._id = id
        self.title = title
        self.url = url


class FoodModel(db.Model):
    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.Text())

    def __init__(self, name, description):
        self.name = name
        self.description = description


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
