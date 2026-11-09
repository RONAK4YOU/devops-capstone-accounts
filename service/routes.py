"""REST endpoints for account CRUD operations."""

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from service import db
from service.models import Account

accounts_bp = Blueprint("accounts", __name__)


def error(message, status):
    return jsonify({"error": message}), status


@accounts_bp.post("/accounts")
def create_account():
    data = request.get_json(silent=True) or {}
    if not data.get("name") or not data.get("email"):
        return error("name and email are required", 400)
    account = Account(name=data["name"].strip(), email=data["email"].strip().lower(),
                      address=data.get("address"))
    db.session.add(account)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error("email already exists", 409)
    return jsonify(account.to_dict()), 201


@accounts_bp.get("/accounts")
def list_accounts():
    return jsonify([account.to_dict() for account in Account.query.order_by(Account.id).all()])


@accounts_bp.get("/accounts/<int:account_id>")
def read_account(account_id):
    account = db.session.get(Account, account_id)
    if account is None:
        return error("account not found", 404)
    return jsonify(account.to_dict())


@accounts_bp.put("/accounts/<int:account_id>")
def update_account(account_id):
    account = db.session.get(Account, account_id)
    if account is None:
        return error("account not found", 404)
    data = request.get_json(silent=True) or {}
    for field in ("name", "email", "address"):
        if field in data:
            value = data[field]
            if field in ("name", "email") and not value:
                return error(f"{field} cannot be empty", 400)
            setattr(account, field, value.strip().lower() if field == "email" else value)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error("email already exists", 409)
    return jsonify(account.to_dict())


@accounts_bp.delete("/accounts/<int:account_id>")
def delete_account(account_id):
    account = db.session.get(Account, account_id)
    if account is None:
        return error("account not found", 404)
    db.session.delete(account)
    db.session.commit()
    return "", 204
