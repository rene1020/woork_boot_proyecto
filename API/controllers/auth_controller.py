from ..models.user_model import User
from ..models.exceptions import NameConflictError, UnauthorizedAccess, InvalidDataError, NotFound, ForbiddenAction
from functools import wraps
from flask import request, jsonify, session
from werkzeug.security import generate_password_hash


class AuthController:
    @classmethod
    def register(cls):
        user_data = request.json
        new_user = User.validate_data(user_data)

        if User.check_user(user_data.get('username')):
            raise NameConflictError('user', 'username', user_data.get('username'))

        User.create_user(new_user)
        return jsonify({'message': 'User created successfully'}), 201
    
    @classmethod
    def login(cls):
        data = request.json
        if not User.check_user(data.get('username')):
            raise InvalidDataError(description="Username or Password Incorrect")
        
        user = User(username = data.get('username'), password = data.get('password'))

        if user.is_registered():
            session['user_id'] = user.user_id
            return jsonify({'message': 'Inicio de sesión exitoso'}), 200
        else:
            raise InvalidDataError(description="Username or Password Incorrect")

    @classmethod
    def logout(cls):
        session.pop('user_id', None)
        return jsonify({'message': 'Cierre de sesión exitoso'}), 200
    
    @classmethod
    def show_profile(cls):
        user_id = session.get('user_id')
        user = User.get_user(user_id)
        if user is None:
            return NotFound(user_id, "user")
        else:
            return jsonify(user.serialize()), 200

    @classmethod
    def login_required(cls, func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if 'user_id' not in session:
                raise UnauthorizedAccess()
            return func(*args, **kwargs)
        return decorated_view
    
    
    @classmethod
    def change_password(cls):
        user_data = request.json
        old_password = user_data.get('old_password')
        new_password = user_data.get('new_password')
        user = User.get_user(session['user_id'])
        user.password = old_password
        if user.is_registered():
            User.update_password((generate_password_hash(new_password), session['user_id']))
            return jsonify({"message": "User updated successfully"}), 200
        else:
            raise ForbiddenAction()
    