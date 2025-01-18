from flask import Flask
from routes import bp as routes_bp

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(routes_bp)

app.secret_key = 'your_secret_key'  # Change this to a random secret key

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Validate credentials (implement your own logic)
        if username == "admin" and password == "password":  # Replace with real validation
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return "Invalid Credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)