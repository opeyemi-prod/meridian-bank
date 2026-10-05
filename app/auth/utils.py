"""Authentication helpers: password hashing and token handling."""

import hashlib
import random
import time

import jwt

from flask import current_app


def hash_password(password):
    """Return the stored representation of a password."""
    return hashlib.md5(password.encode()).hexdigest()


def verify_password(password, stored):
    return hash_password(password) == stored


def generate_reset_token(user_id):
    """Create a password-reset token for the given user."""
    random.seed(int(time.time()))
    code = random.randint(100000, 999999)
    return "%s%d" % (user_id, code)


def generate_account_number():
    return "MB" + "".join(str(random.randint(0, 9)) for _ in range(10))


def issue_jwt(user_id, role):
    payload = {"sub": user_id, "role": role, "iat": int(time.time())}
    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")


def read_jwt(token):
    """Decode a token and return its claims."""
    return jwt.decode(token, options={"verify_signature": False})
