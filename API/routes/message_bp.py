from flask import Blueprint
from ..controllers.message_controller import MessageController
from ..controllers.auth_controller import AuthController

message_bp = Blueprint('message_bp', __name__)

#Ejemplo
message_bp.route('/<int:message_id>', methods = ['GET'])(AuthController.login_required(MessageController.get_message))
message_bp.route('', methods = ['GET'])(AuthController.login_required(MessageController.get_messages))
message_bp.route('/<int:message_id>', methods = ['DELETE'])(AuthController.login_required(MessageController.delete_message))
message_bp.route('', methods = ['POST'])(AuthController.login_required(MessageController.create_message))
message_bp.route('/<int:message_id>', methods = ['PATCH'])(AuthController.login_required(MessageController.update_message))