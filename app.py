from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "kirana-secret-key"

# ---------- DATABASE CONFIG ----------
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root123@localhost/user_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------- MODELS ----------

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(255))


class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    day = db.Column(db.String(20))
    meal_type = db.Column(db.String(20))
    meal_name = db.Column(db.String(100))


# ---------- ROUTES ----------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if User.query.filter_by(email=request.form['email']).first():
            flash("Email already exists")
            return redirect('/signup')

        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password_hash=generate_password_hash(request.form['password'])
        )
        db.session.add(user)
        db.session.commit()

        flash("Signup successful. Please login.")
        return redirect('/login')

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()

        if user and check_password_hash(user.password_hash, request.form['password']):
            session['user_id'] = user.id
            return redirect('/dashboard')

        flash("Invalid email or password")
        return redirect('/login')

    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    user = User.query.get(session['user_id'])

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    meal_types = ["Breakfast","Lunch","Dinner"]

    # ---------- SAVE / OVERWRITE MEAL ----------
    if request.method == 'POST':
        day = request.form['day']
        meal_type = request.form['meal_type']
        meal_name = request.form['meal_name'].strip().title()

        existing = Meal.query.filter_by(
            user_id=user.id,
            day=day,
            meal_type=meal_type
        ).first()

        if existing:
            existing.meal_name = meal_name
        else:
            db.session.add(Meal(
                user_id=user.id,
                day=day,
                meal_type=meal_type,
                meal_name=meal_name
            ))

        db.session.commit()
        return redirect('/dashboard')

    # ---------- BUILD WEEKLY GRID ----------
    meals = Meal.query.filter_by(user_id=user.id).all()

    weekly = {d: {m: None for m in meal_types} for d in days}

    for meal in meals:
        weekly[meal.day][meal.meal_type] = meal

    return render_template(
        'dashboard.html',
        user=user,
        weekly=weekly,
        meal_types=meal_types
    )


@app.route('/clear-meals', methods=['POST'])
def clear_meals():
    if 'user_id' not in session:
        return redirect('/login')

    Meal.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# ---------- RUN ----------
if __name__ == '__main__':
    app.run(debug=True)
