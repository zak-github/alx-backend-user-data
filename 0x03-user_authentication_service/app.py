#!/usr/bin/env python3
"""
A python Flask Module
"""
from auth import Auth
from flask import Flask, abort, jsonify, redirect, request

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def getMessage() -> str:
    """ GET /
    Return:
      - {"message": "Bienvenue"}
    """
    return jsonify(message="Bienvenue")


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """ POST /users
    Return:
        - registered user emails
    """
    try:
        email = request.form['email']
        password = request.form['password']
        user = AUTH.register_user(email=email, password=password)
        return jsonify(email=user.email, message='user created'), 200
    except ValueError:
        return jsonify(message='email already registered'), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /sessions
    Return:
        - login user email
    """
    try:
        email = request.form['email']
        password = request.form['password']
        if AUTH.valid_login(email=email, password=password):
            session_id = AUTH.create_session(email=email)
            response = jsonify(email=email, message='logged in')
            response.set_cookie('session_id', session_id)
            return response
        else:
            abort(401)
    except Exception:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ DELETE /sessions
    Return:
        - destroy session and redirect to GET /
    """
    try:
        session_id = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(session_id=session_id)
        AUTH.destroy_session(user.id)
        return redirect('/')
    except Exception:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ GET /profile
    Return:
        - profile user
    """
    try:
        session_id = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(session_id=session_id)
        return jsonify(email=user.email), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """ POST /reset_password
    Return:
        - reset password token
    """
    try:
        email = request.form['email']
        token = AUTH.get_reset_password_token(email=email)
        return jsonify(email=email, reset_token=token), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """ PUT /reset_password
    Return:
        - update password
    """
    try:
        email = request.form['email']
        token = request.form['reset_token']
        new_password = request.form['new_password']
        AUTH.update_password(reset_token=token, password=new_password)
        return jsonify(email=email, message='Password updated'), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
