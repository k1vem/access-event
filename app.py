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
