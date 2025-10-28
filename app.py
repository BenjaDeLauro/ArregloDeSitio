from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from extensions import db   # ⬅️ usar el db compartido

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"   # o tu MySQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)            # ⬅️ importante
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/users', methods=['GET', 'POST'])
def users():
    from models import User   # import local para evitar ciclo

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        if username and email:
            try:
                nuevo = User(username=username, email=email)
                db.session.add(nuevo)
                db.session.commit()
                return redirect(url_for('users'))  # PRG
            except Exception as e:
                db.session.rollback()
                print(f"[ERROR] No se pudo guardar usuario: {e}")

    usuarios = User.query.order_by(User.id.desc()).all()
    return render_template('users.html', users=usuarios)

if __name__ == '__main__':
    # Crear tablas la primera vez
    with app.app_context():
        from models import User, Post, Comment  # asegura el registro de modelos
        db.create_all()
    app.run(debug=True)
