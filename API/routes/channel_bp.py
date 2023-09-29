"""Channel Blueprint"""

from flask import Blueprint
from ..controllers.channel_controller import ChannelController
from ..controllers.auth_controller import AuthController

channel_bp = Blueprint("channel_bp", __name__)

channel_bp.route("", methods=["POST"])(
    AuthController.login_required(ChannelController.create_channel)
)
channel_bp.route("", methods=["GET"])(
    AuthController.login_required(ChannelController.get_channels)
)
channel_bp.route("/<int:channel_id>", methods=["GET"])(
    AuthController.login_required(ChannelController.get_channel)
)
channel_bp.route("/<int:channel_id>", methods=["PUT"])(
    AuthController.login_required(ChannelController.update_channel)
)
channel_bp.route("/<int:channel_id>", methods=["DELETE"])(
    AuthController.login_required(ChannelController.delete_channel)
)
