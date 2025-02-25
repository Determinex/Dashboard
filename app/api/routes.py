# api/routes.py

from flask import jsonify # Import jsonify function from Flask

# Define the API routes
def register_routes(api):
    @api.get('/api/hello')
    def hello():
        # Logic to retrieve items from the database (placeholder)
        return jsonify({'message': 'Hello, World!'})

    @api.get('/api/items')
    def get_items():
        items = [{'id': 1, 'name': 'Item 1'}, {'id': 2, 'name': 'Item 2'}]
        # Logic to retrieve items from the database (placeholder)
        return jsonify(items)

    @api.post('/api/items')
    def create_item():
        # Logic to create a new item (placeholder)
        return jsonify({'message': 'Item created successfully.'}), 201