
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request, redirect, session, flash, jsonify, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import numpy as np
import joblib
from responses import DISEASE_RESPONSES
from leftover import get_suggestions
from grocery import generate_weekly_grocery
from nutrition_calc import analyze_family_balance
from meal_name import get_all_meal_names
import random
import string
from meal_ingredients_v2 import MEAL_INGREDIENTS




# ---------- APP CONFIG ----------

app = Flask(__name__)
app.secret_key = "kirana-secret-key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root123@localhost/user_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ---------- MAIL CONFIG ----------
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME="forkirana2026@gmail.com",
    MAIL_PASSWORD="rzas fqjj jlnv kxtb"
)

db = SQLAlchemy(app)
mail = Mail(app)

serializer = URLSafeTimedSerializer(app.secret_key)

# ---------- MODELS ----------

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)  # ✅ EMAIL VERIFICATION


class Meal(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    week_start_date = db.Column(db.Date, nullable=False)  # ✅ NEW

    day = db.Column(db.String(20))
    meal_type = db.Column(db.String(20))
    meal_name = db.Column(db.String(100))
    persons = db.Column(db.Integer, default=1)
    __table_args__ = (
    db.UniqueConstraint(
        'user_id',
        'week_start_date',
        'day',
        'meal_type',
        name='unique_meal_per_week'
    ),
)

class GroceryList(db.Model):
    __tablename__ = 'grocery_list'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_name = db.Column(db.String(100))
    quantity = db.Column(db.String(50))
    week_start_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class MealLibrary(db.Model):
    __tablename__ = "meal_library"

    id = db.Column(db.Integer, primary_key=True)
    meal_name = db.Column(db.String(100), nullable=False, unique=True)

class DayPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    day = db.Column(db.String(20), nullable=False)
    persons = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class WeeklyPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    day = db.Column(db.String(20))
    persons = db.Column(db.Integer)
# ---------- EMAIL VERIFICATION HELPERS ----------

def generate_token(email):
    return serializer.dumps(email, salt="email-verify")

def confirm_token(token, expiration=3600):
    try:
        return serializer.loads(token, salt="email-verify", max_age=expiration)
    except:
        return None

def send_verification_email(email):
    token = generate_token(email)
    link = url_for("verify_email", token=token, _external=True)

    msg = Message(
        "Verify your email",
        sender=app.config["MAIL_USERNAME"],
        recipients=[email]
    )
    msg.body = f"Click the link to verify your account:\n{link}"
    mail.send(msg)

# ---------- LOAD CHATBOT MODEL ----------
try:
    chatbot_model = joblib.load("intent_model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    print("✅ Chatbot model loaded successfully")
except Exception as e:
    print("❌ Model load error:", e)
    chatbot_model = None
    vectorizer = None


def chatbot_reply(user_input):
    if chatbot_model is None or vectorizer is None:
        return "Chatbot model not available."

    user_input = user_input.strip()

    if not user_input:
        return "Please enter a message."

    try:
        vectorized = vectorizer.transform([user_input])
        prediction = chatbot_model.predict(vectorized)[0]

        # 🔍 DEBUG PRINTS
        print("Predicted intent:", prediction)
        print("Available response keys:", DISEASE_RESPONSES.keys())

        return DISEASE_RESPONSES.get(
            prediction,
            "I didn't understand that. Please ask about a listed condition."
        )

    except Exception as e:
        print("CHATBOT ERROR:", e)
        return "⚠️ System Error. Please try again."
# ---------- ROUTES ----------

@app.route("/")
def index():
    return render_template("index.html")

# ---------- SIGNUP ----------

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        confirm_password = request.form.get('confirm_password').strip()

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for('signup'))
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.")
            return redirect(url_for('signup'))
        hashed_password = generate_password_hash(password)

        new_user = User(
            name=name,
            email=email,
            password_hash=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully. Please login.")
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()

        if user and check_password_hash(user.password_hash, request.form['password']):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))

        flash("Invalid email or password")

    return render_template('login.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("No account found with that email.")
            return redirect(url_for('forgot_password'))

        # Generate a temporary token (for demo, simple random string)
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

        # Construct reset link
        reset_link = url_for('reset_password', token=token, email=user.email, _external=True)

        # Send email
        try:
            from flask_mail import Message
            msg = Message(
                subject="Reset Your Password",
                sender=app.config['MAIL_USERNAME'],
                recipients=[email],
                html=f"""
                    <p>Hi {user.name},</p>
                    <p>Click the link below to reset your password:</p>
                    <a href="{reset_link}">{reset_link}</a>
                    <p>If you didn't request this, ignore this email.</p>
                """
            )
            mail.send(msg)
            flash("Password reset link sent to your email.")
        except Exception as e:
            flash(f"Error sending email: {e}")

        return redirect(url_for('login'))

    return render_template('forgot_password.html')


#------- reset password-------------
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # In production, verify token validity and expiry here
    if request.method == 'POST':
        new_password = request.form.get('password').strip()
        confirm_password = request.form.get('confirm_password').strip()

        if new_password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for('reset_password', token=token))

        # For demo: assume token maps to a user email
        # In a real app, fetch user by token from DB
        user_email = request.args.get('email')  # replace with DB lookup
        user = User.query.filter_by(email=user_email).first()
        if not user:
            flash("Invalid token or user not found.")
            return redirect(url_for('login'))

        user.password_hash = generate_password_hash(new_password)
        db.session.commit()

        flash("Password updated successfully. You can now login.")
        return redirect(url_for('login'))

    return render_template('reset_password.html', token=token)

#-----------grocery---------------
@app.route('/grocery')
def grocery():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    meals = Meal.query.filter_by(user_id=user_id).all()

    if not meals:
        flash("No meals found.")
        return redirect(url_for('dashboard'))

    today = date.today()
    week_start = today - timedelta(days=today.weekday())

    grocery_data = {}

    for meal in meals:
        meal_grocery = generate_weekly_grocery([meal], meal.persons)

        for item, data in meal_grocery.items():
            # 🔥 Skip non-grocery items
            if item.lower() in ["water"]:
                continue

            if item not in grocery_data:
                grocery_data[item] = data
            else:
                grocery_data[item]["qty"] += data["qty"]

    GroceryList.query.filter_by(
        user_id=user_id,
        week_start_date=week_start
    ).delete()

    for item, data in grocery_data.items():
        db.session.add(GroceryList(
            user_id=user_id,
            item_name=item,
            quantity=str(data["qty"]),
            week_start_date=week_start
        ))

    db.session.commit()

    return render_template("grocery.html", grocery_list=grocery_data)

# ---------- LOGOUT ----------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------- DASHBOARD ----------

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    meal_types = ["Breakfast", "Lunch", "Dinner"]
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    
    # 🔥 BULLETPROOF - Check if user has existing plan
    first_plan = db.session.query(DayPlan.id).filter_by(user_id=user_id).first()
    plan_created_date = None
    days_since_creation = 0

    if first_plan:
        days_since_creation = 1  # Plan exists = Day 1
        plan_created_date = today
    else:
        days_since_creation = 0  # No plan
        plan_created_date = None

    if request.method == 'POST':
        day = request.form.get("day")
        meal_type = request.form.get("meal_type")
        meal_name = request.form.get("meal_name")
        persons = int(request.form.get("persons", 1))

        if day and meal_type and meal_name:
            # Filter by week also
            existing_meal = Meal.query.filter_by(
                user_id=user_id,
                week_start_date=week_start,
                day=day,
                meal_type=meal_type
            ).first()

            if existing_meal:
                existing_meal.meal_name = meal_name
                existing_meal.persons = persons
            else:
                new_meal = Meal(
                    user_id=user_id,
                    week_start_date=week_start,
                    day=day,
                    meal_type=meal_type,
                    meal_name=meal_name,
                    persons=persons
                )
                db.session.add(new_meal)

            db.session.commit()
            flash("Meal saved successfully!")
            return redirect(url_for('dashboard'))

    # Only load meals for current week
    meals = Meal.query.filter_by(
    user_id=user_id,
    week_start_date=week_start
).all()

    weekly = {day: {} for day in days}
    weekly_persons = {day: 1 for day in days}

    for meal in meals:
        weekly[meal.day][meal.meal_type] = meal.meal_name
        weekly_persons[meal.day] = meal.persons

    summary = analyze_family_balance(meals, weekly_persons)

    return render_template(
        "dashboard.html",
        user=user,
        weekly=weekly,
        weekly_persons=weekly_persons,
        days=days,
        meal_types=meal_types,
        summary=summary,
        today=today,
        plan_created_date=plan_created_date,
        days_since_creation=days_since_creation,
        week_start=week_start  
    )

@app.route('/clear-meals', methods=['POST'])
def clear_meals():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    Meal.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()

    return redirect(url_for('dashboard'))

@app.route("/update_persons", methods=["POST"])
def update_persons():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    day = request.form.get("day")
    persons = int(request.form.get("persons"))

    today = date.today()
    week_start = today - timedelta(days=today.weekday())

    meals = Meal.query.filter_by(
        user_id=user_id,
        week_start_date=week_start,
        day=day
    ).all()

    for meal in meals:
        meal.persons = persons

    db.session.commit()

    return redirect(url_for("dashboard"))
#-----------
@app.route('/create_week', methods=['POST'])
def create_week():
    user_id = session['user_id']
    
    # Clear old DayPlans
    DayPlan.query.filter_by(user_id=user_id).delete()
    
    # Create 7 new days
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in days:
        day_plan = DayPlan(user_id=user_id, day=day, persons=1)
        db.session.add(day_plan)
    
    db.session.commit()
    flash('✅ Week created successfully!')
    return redirect(url_for('dashboard'))

# ---------- NUTRITION ----------

@app.route('/nutrition')
def nutrition_analysis():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    meals = Meal.query.filter_by(user_id=user_id).all()

    weekly_persons = {}

    for day in days:
        plan = DayPlan.query.filter_by(
            user_id=user_id,
            day=day
        ).first()

        weekly_persons[day] = plan.persons if plan else 1

    result = analyze_family_balance(meals, weekly_persons)

    return render_template(
        'nutrition.html',
        stats=result.get("summary", {}),
        recommendations=result.get("recommendations", [])
    )
#-----leftover--------------

@app.route('/suggest', methods=['GET', 'POST'])
def suggest_recipes():

    suggestions = []

    if request.method == 'POST':
        user_ingredients_str = request.form.get('user_ingredients', '')

        user_has = [i.strip().lower() for i in user_ingredients_str.split(",") if i.strip()]

        for meal_name, recipe_dict in MEAL_INGREDIENTS.items():
            recipe_ingredients = list(recipe_dict.keys())
            total_needed = len(recipe_ingredients)

            matches = [i for i in recipe_ingredients if i in user_has]
            missing = [i for i in recipe_ingredients if i not in user_has]

            if matches:
                score = (len(matches) / total_needed * 100) 
                suggestions.append({
                    "meal": meal_name.title(),
                    "score": round(score), 
                    "missing": [m.title() for m in missing]
                })

    return render_template("leftover.html", suggestions=suggestions)

#-----------meal library------
@app.route('/meal_name')
def meal_name():
    query = request.args.get('q', '').lower()

    names = [m.replace("_", " ").title() for m in MEAL_INGREDIENTS.keys()]
    names.sort()

    if query:
        names = [m for m in names if query in m.lower()]

    return render_template("meal_name.html", meals=names)

# ---------- CHATBOT ----------

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    if "user_id" not in session:
        return redirect("/login")

    # When page loads
    if request.method == "GET":
        return render_template("chatbot.html")

    # When JS sends message
    if request.method == "POST":
        data = request.get_json()
        message = data.get("message", "")

        reply = chatbot_reply(message)

        return jsonify({"reply": reply})

# ---------- RUN ----------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)