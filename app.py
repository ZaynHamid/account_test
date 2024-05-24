
# import logging
# from flask import Flask, request, jsonify, url_for, session, g
# import mysql.connector
# from flask_bcrypt import Bcrypt
# from flask_mail import Mail, Message
# from flask_cors import CORS
# from flask_session import Session
# import string
# import random
# import secrets
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# # Configuration for Flask-Session
# app.config['SESSION_TYPE'] = 'filesystem'  # Set the appropriate session type
# app.config['SESSION_FILE_DIR'] = '/tmp/flask_session/'  # Directory for filesystem sessions

# # Other configurations
# app.secret_key = "!@#PPBigertandu"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# bcrypt = Bcrypt(app)
# CORS(app)

# # Initialize Flask-Session
# Session(app)

# db = SQLAlchemy(app)

# class users(db.Model):
#     _id = db.Column("id", db.Integer, primary_key =True)
#     name = db.Column("name", db.String(255))
#     email = db.Column("email", db.String(255))
#     password = db.Column("password", db.String(255))
#     notes = db.Column("note", db.String(60000))
    
#     def __init__(self, name, email, password, notes):
#         self.name = name
#         self.email = email
#         self.password = password
#         self.notes = notes
        




# # Mail configuration
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = 'waleedhamid444@gmail.com'
# app.config['MAIL_PASSWORD'] = 'dqykwdrptwhzrpsl'
# mail = Mail(app)

# @app.route("/")
# def home():
#     return "Hi"

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     data = request.json
#     identifier = data.get('identifier')
#     password = data.get('password')

#     if '@' in identifier:
#         query = 'SELECT name, pswd, email FROM user WHERE email = %s'
#     else:
#         query = 'SELECT name, pswd, email FROM user WHERE name = %s'

#     db = get_db()
#     cursor = db.cursor()

#     cursor.execute(query, (identifier,))
#     user = cursor.fetchone()

#     if user:
#         stored_username, stored_password, email = user
#         if bcrypt.check_password_hash(stored_password, password):
#             session['username'] = stored_username
#             return jsonify({'success': True, 'message': 'Login successful', 'email': email, 'user': stored_username})
#         else:
#             return jsonify({'success': False, 'message': 'Invalid username or password. Try again or click Forgot Password.'})
#     else:
#         return jsonify({'success': False, 'message': "Couldn't find your ZPad Account. Please sign up to create one."})

# def generate_verification_code():
#     return ''.join(random.choices(string.digits, k=6))

# @app.route('/signup', methods=['POST'])
# def signup():
#     data = request.json
#     email = data.get("email")
#     username = data.get("username")
#     password = data.get("password")

#     db = get_db()
#     cursor = db.cursor()

#     sql_user_exist = 'SELECT * FROM user WHERE email = %s'
#     cursor.execute(sql_user_exist, (email,))
#     existing_user = cursor.fetchone()

#     if existing_user:
#         return jsonify({'success': False, 'message': 'User already exists!'})

#     sql_username_exist = 'SELECT * FROM user WHERE name = %s'
#     cursor.execute(sql_username_exist, (username,))
#     existing_username = cursor.fetchone()
#     if existing_username:
#         return jsonify({'success': False, 'message': 'Username is taken, please try a different one.'})

#     verification_code = generate_verification_code()
#     session['verification_code'] = verification_code
#     session['email'] = email
#     session['username'] = username
#     session['password'] = bcrypt.generate_password_hash(password).decode('utf-8')

#     msg = Message('Verify your email', sender='waleedhamid444@gmail.com', recipients=[email])
#     msg.body = f'Your verification code is {verification_code}'
#     mail.send(msg)

#     return jsonify({'success': True, 'message': 'Verification code sent to your email!'})

# @app.route('/verify', methods=['POST'])
# def verify():
#     data = request.json
#     code = data.get("code")

#     stored_code = session.get('verification_code')
#     if code == stored_code:
#         db = get_db()
#         cursor = db.cursor()

#         email = session.get('email')
#         username = session.get('username')
#         hashed_pswd = session.get('password')

#         sql = "INSERT INTO user (name, email, pswd, data) VALUES (%s, %s, %s, %s)"
#         val = (username, email, hashed_pswd, f'Hello! {username}')
#         cursor.execute(sql, val)
#         db.commit()

#         session.pop('verification_code', None)
#         session.pop('email', None)
#         session.pop('username', None)
#         session.pop('password', None)

#         return jsonify({'success': True, 'message': 'Account Created!'})
#     else:
#         return jsonify({'success': False, 'message': 'Invalid verification code'})

# def generate_token(length=30):
#     characters = string.ascii_letters + string.digits
#     return ''.join(secrets.choice(characters) for i in range(length))

# @app.route('/delete_account', methods=['POST'])
# def delete_account():
#     data = request.json
#     username = data.get("username")

#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute('DELETE FROM user WHERE name = %s', (username,))
#     db.commit()
#     return jsonify({'success': True, 'message': 'Successfully deleted account!', 'redirect_url': url_for('login')})

# @app.route('/forgot_password', methods=['POST'])
# def forgot_password():
#     data = request.json
#     email = data.get('email')

#     db = get_db()
#     cursor = db.cursor()
#     sql_user_exist = 'SELECT * FROM user WHERE email = %s'
#     cursor.execute(sql_user_exist, (email,))

#     existing_user = cursor.fetchall()
#     if existing_user:
#         reset_token = generate_token()

#         reset_link = f'http://localhost:3000/reset_password/{reset_token}'
#         session['reset_token'] = reset_token
#         session['email'] = email
#         msg = Message('Password Reset Request', sender='waleedhamid444@gmail.com', recipients=[email])
#         msg.body = f'Click the following link to reset your password: {reset_link}'
#         mail.send(msg)
#         return jsonify({'success': True, 'message': 'A reset link has been sent to your email!',  'redirect_url': url_for('login')})
#     else:
#         return jsonify({'success': False, 'message': 'User does not exist!'})

# @app.route("/reset_password", methods=['POST'])
# def reset_password():
#     data = request.json
#     new_password = data.get("password")
#     confirm_password = data.get('confirmPassword')

#     db = get_db()
#     cursor = db.cursor()

#     stored_token = session.get("reset_token")
#     email = session.get("email")

#     if stored_token and email:
#         if new_password == confirm_password:
#             hashed_pswd = bcrypt.generate_password_hash(new_password)
#             cursor.execute('UPDATE user SET pswd = %s WHERE email = %s', (hashed_pswd, email,))
#             db.commit()
#             session.pop("reset_token")
#             session.pop("email")
#             return jsonify({'success': True, 'message': 'Password Changed Successfully', 'redirect_url': url_for('login')})
#         else:
#             return jsonify({'success': False, 'message': 'Passwords don\'t match!'})
#     else:
#         return jsonify({'success': False, 'message': 'Invalid or expired token'})

# @app.route('/save', methods=['POST'])
# def save_to_db():
#     data = request.json
#     val = data.get('inputVal')
#     user = data.get('user')

#     db = get_db()
#     cursor = db.cursor()

#     cursor.execute('SELECT * FROM user WHERE name = %s', (user,))
#     user_exist = cursor.fetchone()
#     if user_exist:
#         cursor.execute('UPDATE user SET data = %s WHERE name = %s', (val, user,))
#         db.commit()
#         return jsonify({'success': True, 'message': 'Changes Saved!'})
#     else:
#         return jsonify({'success': False, 'message': 'User not found'})

# @app.route("/get_note", methods=['POST'])
# def get_note():
#     try:
#         data = request.json
#         user = data.get('parsedEmail')

#         db = get_db()
#         cursor = db.cursor()

#         if not user:
#             return jsonify({'success': False, 'message': 'User field is missing in the request'}), 400

#         cursor.execute('SELECT data FROM user WHERE email = %s', (user,))
#         note = cursor.fetchone()

#         if note:
#             return jsonify({'success': True, 'message': 'Note retrieved', 'data': note[0]})
#         else:
#             return jsonify({'success': False, 'message': 'Note not found'}), 404
#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#         return jsonify({'success': False, 'message': 'An error occurred'}), 500


# if __name__ == '__main__':
#     app.run(debug=True)

import logging
from flask import Flask, request, jsonify, session, url_for
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from flask_cors import CORS
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import string
import random
import secrets

app = Flask(__name__)

# Configuration for Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'  # Set the appropriate session type
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session/'  # Directory for filesystem sessions

# Other configurations
app.secret_key = "!@#PPBigertandu"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)
CORS(app)

# Initialize Flask-Session
Session(app)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.String(60000), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'waleedhamid444@gmail.com'
app.config['MAIL_PASSWORD'] = 'dqykwdrptwhzrpsl'
mail = Mail(app)

@app.route("/")
def home():
    return "Hi"

@app.route('/login', methods=['POST', 'GET'])
def login():
    data = request.json
    identifier = data.get('identifier')
    password = data.get('password')

    user = User.query.filter_by(email=identifier).first() or User.query.filter_by(name=identifier).first()

    if user and bcrypt.check_password_hash(user.password, password):
        session['username'] = user.name
        return jsonify({'success': True, 'message': 'Login successful', 'email': user.email, 'user': user.name})
    else:
        return jsonify({'success': False, 'message': "Invalid username or password. Try again or click Forgot Password."})

def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': 'User already exists!'})

    if User.query.filter_by(name=username).first():
        return jsonify({'success': False, 'message': 'Username is taken, please try a different one.'})

    verification_code = generate_verification_code()
    session['verification_code'] = verification_code
    session['email'] = email
    session['username'] = username
    session['password'] = bcrypt.generate_password_hash(password).decode('utf-8')

    msg = Message('Verify your email', sender='waleedhamid444@gmail.com', recipients=[email])
    msg.body = f'Your verification code is {verification_code}'
    mail.send(msg)

    return jsonify({'success': True, 'message': 'Verification code sent to your email!'})

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    code = data.get("code")

    stored_code = session.get('verification_code')
    if code == stored_code:
        email = session.get('email')
        username = session.get('username')
        hashed_pswd = session.get('password')

        new_user = User(name=username, email=email, password=hashed_pswd, notes=f'Hello! {username}')
        db.session.add(new_user)
        db.session.commit()

        session.pop('verification_code', None)
        session.pop('email', None)
        session.pop('username', None)
        session.pop('password', None)

        return jsonify({'success': True, 'message': 'Account Created!'})
    else:
        return jsonify({'success': False, 'message': 'Invalid verification code'})

def generate_token(length=30):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for i in range(length))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    data = request.json
    username = data.get("username")

    User.query.filter_by(name=username).delete()
    db.session.commit()

    return jsonify({'success': True, 'message': 'Successfully deleted account!', 'redirect_url': url_for('login')})

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')

    user = User.query.filter_by(email=email).first()

    if user:
        reset_token = generate_token()

        reset_link = f'http://localhost:3000/reset_password/{reset_token}'
        session['reset_token'] = reset_token
        session['email'] = email
        msg = Message('Password Reset Request', sender='waleedhamid444@gmail.com', recipients=[email])
        msg.body = f'Click the following link to reset your password: {reset_link}'
        mail.send(msg)
        return jsonify({'success': True, 'message': 'A reset link has been sent to your email!',  'redirect_url': url_for('login')})
    else:
        return jsonify({'success': False, 'message': 'User does not exist!'})

@app.route("/reset_password", methods=['POST'])
def reset_password():
    data = request.json
    new_password = data.get("password")
    confirm_password = data.get('confirmPassword')

    stored_token = session.get("reset_token")
    email = session.get("email")

    if stored_token and email:
        if new_password == confirm_password:
            user = User.query.filter_by(email=email).first()
            user.password = bcrypt.generate_password_hash(new_password)
            db.session.commit()
            session.pop("reset_token")
            session.pop("email")
            return jsonify({'success': True, 'message': 'Password Changed Successfully', 'redirect_url': url_for('login')})
        else:
            return jsonify({'success': False, 'message': 'Passwords don\'t match!'})
    else:
        return jsonify({'success': False, 'message': 'Invalid or expired token'})

@app.route('/save', methods=['POST'])
def save_to_db():
    data = request.json
    val = data.get('inputVal')
    user = data.get('user')

    user = User.query.filter_by(name=user).first()

    if user:
        user.notes = val
        db.session.commit()
        return jsonify({'success': True, 'message': 'Changes Saved!'})
    else:
        return jsonify({'success': False, 'message': 'User not found'})

@app.route("/get_note", methods=['POST'])
def get_note():
    try:
        data = request.json
        user = data.get('parsedEmail')

        if not user:
            return



            return jsonify({'success': False, 'message': 'User field is missing in the request'}), 400

        user = User.query.filter_by(email=user).first()

        if user:
            return jsonify({'success': True, 'message': 'Note retrieved', 'data': user.notes})
        else:
            return jsonify({'success': False, 'message': 'Note not found'}), 404
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

