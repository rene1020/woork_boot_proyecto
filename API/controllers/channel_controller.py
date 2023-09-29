"""Channel Controller"""

from flask import request, jsonify, session
from ..models.channel_model import Channel


class ChannelController:
    """Class Channel Controller"""

    @classmethod
    def create_channel(cls):
        """Create channel"""
        channel_data = request.json
        user_id = session.get("user_id")

        if "channel_name" not in channel_data or "server_id" not in channel_data:
            return jsonify({"message": "Channel name and server_id are required"}), 400

        if Channel.exists_by_name(channel_data.get("channel_name")):
            return jsonify({"message": "Channel with this name already exists"}), 400

        channel = Channel.validate_data(
            {
                "channel_name": channel_data.get("channel_name"),
                "server_id": channel_data.get("server_id"),
                "user_id": user_id,
            }
        )

        Channel.create_channel(channel)
        return jsonify({"message": "Channel created successfully"}), 201

    @classmethod
    def update_channel(cls, channel_id):
        """Update channel"""
        update_data = request.json

        if not Channel.exists(channel_id):
            return jsonify({"message": "Channel not found"}), 404

        new_channel_name = update_data.get("channel_name")

        if "channel_name" in update_data:
            if Channel.exists_by_name(new_channel_name):
                return (
                    jsonify({"message": "Channel with this name already exists"}),
                    400,
                )

            if len(new_channel_name) < 1:
                return (
                    jsonify({"message": "Channel name must not be empty"}),
                    400,
                )

        updated_fields = {"channel_name": new_channel_name}
        Channel.update_channel(channel_id, updated_fields)
        return jsonify({"message": "Channel updated successfully"}), 200

    @classmethod
    def get_channels(cls):
        """Get channels"""
        server_id = request.args.get("server_id")
        channels = Channel.get_channels(server_id)
        response = {"channels": [], "total": 0}

        if channels:
            channels_list = []
            for channel in channels:
                channel_dict = {
                    "channel_id": channel.channel_id,
                    "channel_name": channel.channel_name,
                    "server_id": channel.server_id,
                    "user_id": channel.user_id,
                }
                channels_list.append(channel_dict)

            response["channels"] = channels_list
            response["total"] = len(channels_list)
            return jsonify(response), 200

        return jsonify(response), 200

    @classmethod
    def get_channel(cls, channel_id):
        """Get channel"""
        channel = Channel.get_channel(channel_id)
        if channel:
            channel_dict = {
                "channel_id": channel.channel_id,
                "channel_name": channel.channel_name,
                "server_id": channel.server_id,
                "user_id": channel.user_id,
            }
            return jsonify(channel_dict), 200

        return jsonify({"message": "Channel not found"}), 404

    @classmethod
    def delete_channel(cls, channel_id):
        """Delete channel"""
        if not Channel.exists(channel_id):
            return jsonify({"message": "Channel not found"}), 404

        Channel.delete_channel(channel_id)
        return jsonify({"message": "Channel deleted successfully"}), 204
