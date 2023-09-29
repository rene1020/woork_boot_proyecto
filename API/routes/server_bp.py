"""Server Bp"""

from flask import Blueprint
from ..controllers.server_controller import ServerController
from ..controllers.auth_controller import AuthController

server_bp = Blueprint("server_bp", __name__)

server_bp.route("", methods=["POST"])(
    AuthController.login_required(ServerController.create_server)
)
server_bp.route("", methods=["GET"])(
    AuthController.login_required(ServerController.get_servers)
)
server_bp.route("/<int:server_id>", methods=["GET"])(
    AuthController.login_required(ServerController.get_server)
)
server_bp.route("/<int:server_id>", methods=["PUT"])(
    AuthController.login_required(ServerController.update_server)
)
server_bp.route("/<int:server_id>", methods=["DELETE"])(
    AuthController.login_required(ServerController.delete_server)
)
