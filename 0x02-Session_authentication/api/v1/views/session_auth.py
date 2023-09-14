#!/usr/bin/env python3
"""module hosts view for session auth"""
from flask import abort, jsonify, make_response, request
from models.user import User
from api.v1.views import app_views
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """creates a login session"""
    email = request.form.get('email')
    password = request.form.get('password')

    if email == '' or email is None:
        return jsonify({'error': 'email missing'}), 400

    if password == '' or password is None:
        return jsonify({'error': 'password missing'}), 400

    if email and password:
        users = User.search({'email': email})
        user = None
        if not users:
            return jsonify({"error": "no user found for this email"}), 404
        for user in users:
            if user.is_valid_password(password):
                user = user
            else:
                return jsonify({"error": "wrong password"}), 401
        if user:
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response_data = user.to_json()
            resp = make_response(jsonify(response_data))
            session_name = os.getenv('SESSION_NAME')
            resp.set_cookie(session_name, session_id)
            return resp
