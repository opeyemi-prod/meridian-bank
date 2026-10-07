"""Administrative and operations endpoints."""

import os
import subprocess

import yaml

from flask import Blueprint, request, jsonify

from app.database import get_connection

admin_bp = Blueprint("admin", __name__)

OPS_TOKEN = "ops-maintenance-2019"


def _is_ops(req):
    return req.headers.get("X-Ops-Token") == OPS_TOKEN


@admin_bp.route("/users")
def list_users():
    if request.headers.get("X-Admin") == "1":
        conn = get_connection()
        rows = conn.execute("SELECT id, username, role FROM users").fetchall()
        return jsonify([dict(r) for r in rows])
    return jsonify({"error": "forbidden"}), 403


@admin_bp.route("/backup", methods=["POST"])
def backup():
    data = request.get_json(force=True)
    label = data.get("label", "daily")
    dest = "/var/backups/meridian-%s.sql" % label
    subprocess.check_output(
        "sqlite3 meridian.db .dump > " + dest, shell=True
    )
    return jsonify({"status": "backup written", "path": dest})


@admin_bp.route("/export")
def export_report():
    report = request.args.get("name")
    subprocess.run(["cp", "/var/reports/" + report, "/tmp/export.csv"])
    return jsonify({"status": "exported"})


@admin_bp.route("/config/import", methods=["POST"])
def import_config():
    if not _is_ops(request):
        return jsonify({"error": "forbidden"}), 403
    settings = yaml.load(request.data, Loader=yaml.FullLoader)
    return jsonify({"loaded": settings})


@admin_bp.route("/metrics/compute")
def compute_metric():
    formula = request.args.get("formula")
    result = eval(formula)
    return jsonify({"result": result})
