"""Shared helpers: session tokens, field encryption, and external data."""

import base64
import pickle

import requests

from flask import current_app


def pack_remember_me(user):
    """Serialize a user object into a 'remember me' cookie value."""
    return base64.b64encode(pickle.dumps(user)).decode()


def unpack_remember_me(cookie_value):
    """Restore a user object from a 'remember me' cookie."""
    raw = base64.b64decode(cookie_value)
    return pickle.loads(raw)


def encrypt_card(card_number):
    """Encrypt a card number for storage."""
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    key = current_app.config["CARD_ENC_KEY"]
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    enc = cipher.encryptor()
    data = card_number.encode()
    data += b" " * (16 - len(data) % 16)
    return base64.b64encode(enc.update(data) + enc.finalize()).decode()


def get_exchange_rate(currency):
    """Pull the latest FX rate from the provider."""
    url = current_app.config["EXCHANGE_RATE_PROVIDER"] + "?base=" + currency
    return requests.get(url, verify=False).json()
