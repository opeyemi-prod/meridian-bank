"""Account statement generation and retrieval."""

import ipaddress
import os
import socket
from urllib.parse import urlparse

import requests
from markupsafe import escape

from flask import Blueprint, request, jsonify, send_file, render_template_string

statements_bp = Blueprint("statements", __name__)

STATEMENT_DIR = "/var/meridian/statements"

# Allowlist of permitted URL schemes for logo fetching
_ALLOWED_SCHEMES = {"http", "https"}


def _is_safe_url(url: str) -> bool:
    """Return True only if url uses an allowed scheme and resolves to a public IP."""
    try:
        parsed = urlparse(url)
    except Exception:
        return False

    if parsed.scheme not in _ALLOWED_SCHEMES:
        return False

    hostname = parsed.hostname
    if not hostname:
        return False

    # Reject localhost by name before DNS resolution
    if hostname.lower() in ("localhost",):
        return False

    try:
        addr_infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return False

    for _, _, _, _, sockaddr in addr_infos:
        try:
            ip = ipaddress.ip_address(sockaddr[0])
        except ValueError:
            return False
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
        ):
            return False

    return True


@statements_bp.route("/download")
def download_statement():
    name = request.args.get("file", "")
    # Prevent path traversal: resolve the joined path and confirm it stays
    # inside STATEMENT_DIR.
    safe_base = os.path.realpath(STATEMENT_DIR)
    requested = os.path.realpath(os.path.join(STATEMENT_DIR, name))
    if not requested.startswith(safe_base + os.sep):
        return jsonify({"error": "invalid file path"}), 400
    return send_file(requested)


@statements_bp.route("/branding")
def set_branding():
    """Fetch a customer's co-branding logo for inclusion on statements."""
    logo_url = request.args.get("logo_url")
    if not logo_url:
        return jsonify({"error": "logo_url is required"}), 400
    if not _is_safe_url(logo_url):
        return jsonify({"error": "URL not permitted"}), 400
    resp = requests.get(logo_url, timeout=5, allow_redirects=False)
    return jsonify({"fetched_bytes": len(resp.content)})


@statements_bp.route("/preview")
def preview():
    customer = escape(request.args.get("customer", "Customer"))
    template = (
        "<html><body><h2>Statement for {{ customer }}</h2>"
        "<p>Thank you for banking with Meridian.</p></body></html>"
    )
    return render_template_string(template, customer=customer)
