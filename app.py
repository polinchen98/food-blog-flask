from flask import Flask, render_template, request, flash, url_for, redirect
from flask_restful import Api
from werkzeug.security import generate_password_hash, check_password_hash

from db import db, MenuModel, FoodModel, UserModel
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, login_manager, UserMixin

from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = '>u\xdfzW\xe0\xd3\x991\x9c\xa3\xe4\xb9\xcf1:\xd1T8\xddm\xa3\xcc\x89'
api = Api(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class UserLogin(UserMixin):
    def fromDB(self, user_id):
        self.__user = UserModel.query.filter_by(id=user_id).first()
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user.id)


@app.before_first_request
def create_tables():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id)


@app.route('/')
def index():
    return render_template('index.html',
                           title='MainPage',
                           menu=MenuModel.query.all(),
                           food=FoodModel.query.all())


@app.route('/add_food', methods=["POST", "GET"])
def add_food():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['description']) > 10:
            db.session.add(FoodModel(name=request.form['name'],
                                     description=request.form['description']))
            db.session.commit()
            flash('Рецпт добавлен успешно', category='success')
        else:
            flash('Ошибка добавления рецепта1', category='error')

    return render_template('add_food.html',
                           title='AddFood',
                           menu=MenuModel.query.all())


@app.route('/food/<string:name>')
@login_required
def food(name):
    some_food = FoodModel.query.filter_by(name=name).first()
    return render_template('food.html',
                           food_description=some_food.description,
                           menu=MenuModel.query.all(),
                           title=some_food.name)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if request.method == "POST":
        user = UserModel.query.filter_by(email=request.form['email']).first()
        print(user.email)
        if user and check_password_hash(user.password, request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("index"))

    return render_template("login.html",
                           menu=MenuModel.query.all(),
                           title="Login",
                           form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            psw_hash = generate_password_hash(request.form['psw'])
            db.session.add(UserModel(name=request.form['name'],
                                     email=request.form['email'],
                                     password=psw_hash))
            db.session.commit()
            flash("Вы успешно зарегистрированы", "success")
            return redirect(url_for('login'))
        else:
            flash("Ошибка при добавлении в БД", "error")

    return render_template("register.html", menu=MenuModel.query.all(), title="Register", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
