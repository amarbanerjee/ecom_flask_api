from flask_jwt_extended import jwt_required, get_jwt_identity

# Admin-required decorator
def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user["role"] != "admin":
            return {"msg": "Admin access required"}, 403
        return fn(*args, **kwargs)
    return wrapper
