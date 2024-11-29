from flask import Flask, request, jsonify
from flask_restx import Api, Resource, abort
import yaml

# Initialize Flask App
app = Flask(__name__)
api = Api(app, version="1.0", title="Sample API", description="Authenticated API with OpenAPI Spec")

# Load OpenAPI spec
with open("api_spec.yaml", "r") as file:
    spec = yaml.safe_load(file)

# In-memory data storage
items = []

# Bearer token for authentication (in production, use a secure token management system)
AUTH_TOKEN = "my_secure_token"

# Authentication decorator
def authenticate(func):
    """Decorator to enforce token-based authentication."""
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            abort(401, "Authorization header missing or invalid")
        token = auth_header.split(" ")[1]
        if token != AUTH_TOKEN:
            abort(403, "Invalid or expired token")
        return func(*args, **kwargs)
    return wrapper

# Routes
@api.route("/items")
class ItemList(Resource):
    @authenticate
    def get(self):
        """List all items"""
        return jsonify(items)

    @authenticate
    def post(self):
        """Create a new item"""
        new_item = request.json
        items.append(new_item)
        return jsonify(new_item), 201


@api.route("/items/<int:id>")
class Item(Resource):
    @authenticate
    def get(self, id):
        """Get a specific item by ID"""
        for item in items:
            if item["id"] == id:
                return jsonify(item)
        return {"message": "Item not found"}, 404


# Add OpenAPI spec endpoint
@api.route("/openapi.yaml")
class APISpec(Resource):
    def get(self):
        """Return OpenAPI specification"""
        return jsonify(spec)


if __name__ == "__main__":
    app.run(debug=True)
