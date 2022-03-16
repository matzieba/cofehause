from functools import wraps
from flask import abort
from flask_login import current_user

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #If id is not 1 then return abort with 403 error
        try:
            if current_user.id != 1:
                return abort(403)
        #Otherwise continue with the route function
            return f(*args, **kwargs)
        except AttributeError:
            return abort(403)

    return decorated_function

def loged_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if current_user.is_authenticated == False:
                return abort(403)
            return f(*args, **kwargs)
        except AttributeError:
            return abort(403)
    return decorated_function