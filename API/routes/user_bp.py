from flask import Blueprint
from ..controllers.users_controller import UserController
from ..controllers.auth_controller import AuthController

user_bp = Blueprint("user_bp", __name__)

# Ejemplo
user_bp.route("", methods=["GET"])(
    AuthController.login_required(UserController.get_users)
)
user_bp.route("/<int:user_id>", methods=["GET"])(
    AuthController.login_required(UserController.get_user)
)
user_bp.route("/<int:user_id>", methods=["DELETE"])(
    AuthController.login_required(UserController.delete_user)
)
user_bp.route("/<int:user_id>", methods=["PATCH"])(
    AuthController.login_required(UserController.update_user)
)
user_bp.route("/join", methods=["POST"])(
    AuthController.login_required(UserController.add_user_to_server)
)
user_bp.route("/servers", methods=["GET"])(
    AuthController.login_required(UserController.get_user_servers)
)
