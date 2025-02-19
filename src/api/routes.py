# api/routes.py

def register_routes(app):
    @app.get('/api/hello')
    def hello():
        return {'message': 'Hello, World!'}

    @app.get('/api/items')
    def get_items():
        items = [{'id': 1, 'name': 'Item 1'}, {'id': 2, 'name': 'Item 2'}]
        return items

    @app.post('/api/items')
    def create_item():
        return {'message': 'Item created successfully.'}, 201