from functools import wraps
from flask import abort
from flask_login import current_user

def ensure_correct_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        correct_id = kwargs.get('user_id') or kwargs.get('id')
        if correct_id == current_user.id:
            return fn(*args, **kwargs)
        return abort(401, 'Unauthorized')
    return wrapper