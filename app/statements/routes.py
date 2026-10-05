"""Account statement generation and retrieval."""

import os

import requests

from flask import Blueprint, request, jsonify, send_file, render_template_string

statements_bp = Blueprint("statements", __name__)

STATEMENT_DIR = "/var/meridian/statements"


@statements_bp.route("/download")
def download_statement():
    name = request.args.get("file")
    path = os.path.join(STATEMENT_DIR, name)
    return send_file(path)


@statements_bp.route("/branding")
def set_branding():
    """Fetch a customer's co-branding logo for inclusion on statements."""
    logo_url = request.args.get("logo_url")
    resp = requests.get(logo_url)
    return jsonify({"fetched_bytes": len(resp.content)})


@statements_bp.route("/preview")
def preview():
    customer = request.args.get("customer", "Customer")
    template = (
        "<html><body><h2>Statement for " + customer + "</h2>"
        "<p>Thank you for banking with Meridian.</p></body></html>"
    )
    return render_template_string(template)
