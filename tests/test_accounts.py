"""API behavior tests."""

import unittest

from service import create_app, db


class AccountsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://",
             "WTF_CSRF_ENABLED": False}
        )
        self.client = self.app.test_client()
        self.context = self.app.app_context()
        self.context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def create(self):
        return self.client.post("/accounts", json={"name": "Ada", "email": "ada@example.com"})

    def test_health_and_security_headers(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")
        self.assertIn("X-Content-Type-Options", response.headers)

    def test_cors_preflight(self):
        response = self.client.options(
            "/accounts",
            headers={"Origin": "https://example.com", "Access-Control-Request-Method": "GET"},
        )
        self.assertIn(response.status_code, (200, 204))
        self.assertIn("Access-Control-Allow-Origin", response.headers)

    def test_create_list_read_update_delete(self):
        created = self.create()
        self.assertEqual(created.status_code, 201)
        account_id = created.json["id"]
        self.assertEqual(self.client.get("/accounts").json[0]["email"], "ada@example.com")
        self.assertEqual(self.client.get(f"/accounts/{account_id}").status_code, 200)
        changed = self.client.put(f"/accounts/{account_id}", json={"name": "Ada Lovelace"})
        self.assertEqual(changed.json["name"], "Ada Lovelace")
        self.assertEqual(self.client.delete(f"/accounts/{account_id}").status_code, 204)
        self.assertEqual(self.client.get(f"/accounts/{account_id}").status_code, 404)

    def test_validation_and_duplicates(self):
        self.assertEqual(self.client.post("/accounts", json={}).status_code, 400)
        self.assertEqual(self.create().status_code, 201)
        self.assertEqual(self.create().status_code, 409)
