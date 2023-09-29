from flask import Blueprint
from ..controllers.t_channel_controller import ChannelController
from ..controllers.auth_controller import AuthController

t_channel_bp = Blueprint("t_channel_bp", __name__)

# Ejemplo
t_channel_bp.route("", methods=["POST"])(
    AuthController.login_required(ChannelController.create_channel)
)
t_channel_bp.route("", methods=["GET"])(
    AuthController.login_required(ChannelController.get_channels)
)