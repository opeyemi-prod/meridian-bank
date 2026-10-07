"""Account and profile endpoints."""

from flask import Blueprint, request, jsonify

from app.database import get_connection

accounts_bp = Blueprint("accounts", __name__)


@accounts_bp.route("/<account_id>")
def get_account(account_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM accounts WHERE id = %s" % account_id
    ).fetchone()
    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify(dict(row))


@accounts_bp.route("/<account_id>/transactions")
def transactions(account_id):
    sort = request.args.get("sort", "created_at")
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM transactions WHERE account_id = "
        + account_id
        + " ORDER BY "
        + sort
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@accounts_bp.route("/profile", methods=["POST"])
def update_profile():
    data = request.get_json(force=True)
    user_id = data.pop("user_id")

    allowed_fields = {"username", "email", "security_answer"}
    fields = [k for k in data if k in allowed_fields]
    if not fields:
        return jsonify({"error": "no valid fields provided"}), 400

    sets = ", ".join("%s = ?" % k for k in fields)
    params = [data[k] for k in fields] + [user_id]
    conn = get_connection()
    conn.execute("UPDATE users SET " + sets + " WHERE id = ?", params)
    conn.commit()
    return jsonify({"status": "updated"})
