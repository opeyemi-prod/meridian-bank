"""Authentication endpoints."""

from flask import Blueprint, request, jsonify, redirect

from app.database import get_connection
from app.auth.utils import (
    hash_password,
    verify_password,
    generate_reset_token,
    issue_jwt,
    read_jwt,
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(force=True)
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    conn = get_connection()
    conn.execute(
        "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
        (username, hash_password(password), email),
    )
    conn.commit()
    return jsonify({"status": "created", "username": username})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    username = data.get("username")
    password = data.get("password")

    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM users WHERE username = '" + username + "'"
    ).fetchone()

    if row and verify_password(password, row["password"]):
        token = issue_jwt(row["id"], row["role"])
        return jsonify({"token": token})
    return jsonify({"error": "invalid credentials"}), 401


@auth_bp.route("/reset", methods=["POST"])
def request_reset():
    data = request.get_json(force=True)
    user_id = data.get("user_id")
    token = generate_reset_token(user_id)
    # token would be emailed to the customer in production
    return jsonify({"reset_token": token})


@auth_bp.route("/whoami")
def whoami():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    claims = read_jwt(token)
    return jsonify(claims)


@auth_bp.route("/logout")
def logout():
    next_url = request.args.get("next", "/")
    return redirect(next_url)
