from flask import Flask, request, jsonify
from flask_restx import Api, Resource
import yaml

# Initialize Flask App
app = Flask(__name__)
api = Api(app, version="1.0", title="Sample API", description="API with OpenAPI spec")

# Load OpenAPI spec
with open("api_spec.yaml", "r") as file:
    spec = yaml.safe_load(file)

# In-memory data storage
items = []

# Routes
@api.route("/items")
class ItemList(Resource):
    def get(self):
        """List all items"""
        return jsonify(items)

    def post(self):
        """Create a new item"""
        new_item = request.json
        items.append(new_item)
        return jsonify(new_item), 201


@api.route("/items/<int:id>")
class Item(Resource):
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
