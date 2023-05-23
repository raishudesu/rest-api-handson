from flask import request
from flask import jsonify
from functools import wraps

valid_keys = ['81f949548d77a914c245c0f0bb411be1']

def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'API-Key' in request.headers:
            api_key = request.headers['API-Key']
            if api_key in valid_keys:
                return func(*args, **kwargs)
        respone = jsonify({'message': 'Unauthorized'})
        respone.status_code = 401
        return respone
    return wrapper