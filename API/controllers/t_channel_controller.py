from flask import request, jsonify, session
from ..models.t_channel_model import Channel
from ..models.user_model import User
from ..models.exceptions import NotFound, ForbiddenAction, ServerError, NameConflictError

class ChannelController:
    
    @classmethod
    def create_channel(cls):
        channel_data = request.json
        user_id = session["user_id"]
        
        if Channel.exists_name(channel_data.get("channel_name")):
            raise NameConflictError('channel', 'channel_name', channel_data.get("channel_name"))
        
        Channel.create_channel(Channel(
            channel_name = channel_data.get("channel_name"),
            server_id = channel_data.get("server_id"),
            user_id = user_id))
        
        return jsonify({"message": "Channel created successfully"}), 201
        
    @classmethod
    def get_channels(cls):
        server_id = request.args.get("server_id")
        channels = Channel.get_channels_from_server(server_id)
        response = {}
        
        if channels:
            channels_list = []
            for ch in channels:
                channels_list.append(ch.serialize())
        
            response["channels"] = channels_list
            response["total"] = len(channels_list)
            return jsonify(response), 200

        return jsonify(response), 200