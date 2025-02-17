
from apiflask import APIFlask
from apiflask.decorators import auth_required
from flask import Blueprint
from flask_login import current_user

api_bp = Blueprint('api', __name__, url_prefix='/api') # url_prefix to isolate API routes
api = APIFlask(__name__) #Initialize APIFlask within the blueprint

#Example route:
@api_bp.route('/protected')
@auth_required # Use APIFlask's decorator for authentication
def protected_route():
    return {'message': f'Hello, {current_user.username}!  This is a protected API route.'}

@api_bp.route('/public')
def public_route():
    return {'message': 'This is a public API route.'}