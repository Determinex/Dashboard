from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid
from config import DevelopmentConfig

app = Flask(__name__)
CORS(app)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Load plugins
def load_plugins():
    """Load all plugins from the plugins directory."""
    plugins_dir = os.path.join(os.path.dirname(__file__), 'plugins')
    for plugin in os.listdir(plugins_dir):
        plugin_path = os.path.join(plugins_dir, plugin)
        if os.path.isdir(plugin_path) and plugin != '__pycache__':
            try:
                plugin_module = __import__(f'plugins.{plugin}', fromlist=['blueprint'])
                app.register_blueprint(plugin_module.blueprint)
            except ImportError as e:
                app.logger.error(f"Error importing plugin {plugin}: {e}")
            except AttributeError:
                app.logger.error(f"Plugin {plugin} does not have a blueprint attribute.")

load_plugins()

class User(UserMixin, db.Model):
    """User model for storing user information."""
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=str(uuid.uuid4()))
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check the user's password."""
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    """Create database tables before the first request."""
    db.create_all()

@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        os.makedirs(os.path.join('user_data', user.uuid))
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Render the dashboard page."""
    return render_template('dashboard.html', user=current_user)

@app.route('/profile')
@login_required
def profile():
    """Render the profile page."""
    return render_template('profile.html', user=current_user)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Handle profile editing."""
    if request.method == 'POST':
        current_user.username = request.form['username']
        if request.form['password']:
            current_user.set_password(request.form['password'])
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template('edit_profile.html', user=current_user)

@app.route('/profile/delete', methods=['POST'])
@login_required
def delete_profile():
    """Handle profile deletion."""
    user_id = current_user.id
    user_uuid = current_user.uuid
    logout_user()
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    user_dir = os.path.join('user_data', user_uuid)
    if os.path.exists(user_dir):
        for root, dirs, files in os.walk(user_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(user_dir)
    flash('Profile deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/admin/users')
@login_required
def view_users():
    """Render the view users page for admin."""
    if current_user.username != 'admin':
        return redirect(url_for('dashboard'))
    users = User.query.all()
    return render_template('view_users.html', users=users)

@app.route('/user_data/<uuid>')
@login_required
def user_data(uuid):
    """Render the user data page."""
    if current_user.uuid != uuid and current_user.username != 'admin':
        return redirect(url_for('dashboard'))
    user_dir = os.path.join('user_data', uuid)
    if not os.path.exists(user_dir):
        return "User directory not found.", 404
    files = os.listdir(user_dir)
    return render_template('user_data.html', files=files, uuid=uuid)

if __name__ == '__main__':
    app.run(debug=True)
