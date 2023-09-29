from flask import Blueprint
from ..controllers.auth_controller import AuthController

auth_bp = Blueprint('auth_bp', __name__)

auth_bp.route('/register', methods=['POST'])(AuthController.register)
auth_bp.route('/login', methods=['POST'])(AuthController.login)
auth_bp.route('/logout', methods=['GET'])(AuthController.logout)
auth_bp.route("/profile", methods=["GET"])(AuthController.login_required(AuthController.show_profile))
auth_bp.route("/profile/edit_password", methods=["PATCH"])(AuthController.login_required(AuthController.change_password))
