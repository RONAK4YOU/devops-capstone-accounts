"""Database model for an account."""

from service import db


class Account(db.Model):
    """A customer account record."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(254), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        """Serialize this account for the REST API."""
        return {"id": self.id, "name": self.name, "email": self.email,
                "address": self.address}
