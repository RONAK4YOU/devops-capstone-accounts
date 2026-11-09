"""Run the service on port 8080."""

from service import create_app

app = create_app()
app.run(host="0.0.0.0", port=8080)
