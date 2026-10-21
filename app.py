<<<<<<< HEAD
import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from models import db, User, Event, Registration
from routes.auth import auth_bp
from routes.events import events_bp
from routes.registrations import registrations_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(events_bp)
app.register_blueprint(registrations_bp)

@app.route('/')
def index_page(): return render_template('index.html')

@app.route('/events')
def events_page():
    inclusive_only = request.args.get('inclusive') in ('1', 'true')
    query = Event.query.order_by(Event.event_date)
    if inclusive_only: query = query.filter_by(is_inclusive=True)
    return render_template('events.html', events=query.all())

@app.route('/events/create', methods=['GET', 'POST'])
def create_event_page():
    if 'user_id' not in session: return redirect(url_for('login_page'))
    if request.method == 'POST':
        event_date_str = request.form.get('event_date')
        try:
            event_date = datetime.datetime.strptime(event_date_str, "%Y-%m-%dT%H:%M")
        except:
            return render_template('create_event.html', error='Неверный формат даты'), 400
        event = Event(
            title=request.form.get('title'), description=request.form.get('description'),
            location=request.form.get('location'), event_date=event_date, organizer_id=session['user_id'],
            is_inclusive=request.form.get('is_inclusive') == 'on',
            visual_alerts=request.form.get('is_inclusive') == 'on',
            sign_language=request.form.get('is_inclusive') == 'on'
        )
        db.session.add(event); db.session.commit()
        return redirect(url_for('events_page'))
    return render_template('create_event.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email').lower()).first()
        if user and user.check_password(request.form.get('password')):
            session['user_id'] = user.id; session['role'] = user.role; session['username'] = user.username
            return redirect(url_for('profile_page', user_id=user.id))
        return render_template('login.html', error='Неверный email или пароль'), 401
    return render_template('login.html')

@app.route('/logout')
def logout_page():
    session.clear(); return redirect(url_for('index_page'))

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email').lower()
        password = request.form.get('password')
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email уже занят'), 400
        user = User(username=username, email=email, role=request.form.get('role', 'user'), is_deaf=request.form.get('is_deaf') == 'true')
        user.set_password(password); db.session.add(user); db.session.commit()
        return redirect(url_for('login_page'))
    return render_template('register.html')

@app.route('/profile/<int:user_id>')
def profile_page(user_id):
    user = db.session.get(User, user_id)
    if user is None: return 'Пользователь не найден', 404
    regs = Registration.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, registrations=regs, session=session)

with app.app_context(): db.create_all()
if __name__ == '__main__': app.run(host='0.0.0.0', port=5000, debug=True)
=======
import os
from flask import Flask, jsonify, render_template
from config import get_config
from models import db
from routes.auth import auth_bp, register as register_user, login as login_user
from routes.events import events_bp
from routes.registrations import registrations_bp
from routes.communication import communication_bp

def create_app(config_object=None):
    app = Flask(__name__)
    app.config.from_object(config_object or get_config())
    if os.getenv("TESTING") == "1":
        app.config["TESTING"] = True
    db.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(registrations_bp)
    app.register_blueprint(communication_bp)

    @app.post("/api/register")
    def register_alias():
        return register_user()

    @app.post("/api/login")
    def login_alias():
        return login_user()

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "service": "AccessEvent"})

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/events")
    def events_page():
        return render_template("events.html")

    @app.get("/events/<int:event_id>")
    def event_detail_page(event_id):
        return render_template("event_detail.html", event_id=event_id)

    @app.get("/login")
    def login_page():
        return render_template("login.html")

    @app.get("/register")
    def register_page():
        return render_template("register.html")

    @app.get("/dashboard")
    def dashboard_page():
        return render_template("dashboard.html")

    @app.get("/profile")
    def profile_page():
        return render_template("profile.html")

    with app.app_context():
        db.create_all()
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
>>>>>>> 93f660917251956e4d1be85cd249fe95ff9b5fe6
