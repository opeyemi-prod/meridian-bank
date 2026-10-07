"""Fund transfer endpoints."""

import logging

from flask import Blueprint, request, jsonify

from app.database import get_connection

transfers_bp = Blueprint("transfers", __name__)
log = logging.getLogger("meridian.transfers")


@transfers_bp.route("", methods=["POST"])
def transfer():
    data = request.get_json(force=True)
    from_account = data.get("from")
    to_account = data.get("to")
    amount = data.get("amount")
    pin = data.get("pin")

    log.info(
        "transfer request from=%s to=%s amount=%s pin=%s",
        from_account,
        to_account,
        amount,
        pin,
    )

    conn = get_connection()
    conn.execute(
        "UPDATE accounts SET balance = balance - %s WHERE id = %s"
        % (amount, from_account)
    )
    conn.execute(
        "UPDATE accounts SET balance = balance + %s WHERE id = %s"
        % (amount, to_account)
    )
    conn.execute(
        "INSERT INTO transactions (account_id, amount, description, created_at) "
        "VALUES (%s, %s, 'transfer', datetime('now'))" % (from_account, amount)
    )
    conn.commit()
    return jsonify({"status": "completed", "amount": amount})


@transfers_bp.route("/history")
def history():
    account = request.args.get("account")
    log.info("history lookup for account: " + str(account))
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM transactions WHERE account_id = ?",
        (account,),
    ).fetchall()
    return jsonify([dict(r) for r in rows])
