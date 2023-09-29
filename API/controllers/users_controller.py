from ..models.user_model import User
from ..models.server_model import Server
from flask import request, jsonify, session
from ..models.exceptions import NotFound, ForbiddenAction
from werkzeug.utils import secure_filename
import os
from config import Config
import base64


class UserController:
    @classmethod
    def get_users(cls):
        server_id = request.args.get("server_id")
        users = User.get_users(server_id)
        response = {}

        if users:
            users_list = []
            for user in users:
                users_list.append(user.serialize())

            response["users"] = users_list
            response["total"] = len(users_list)
            return jsonify(response), 200
        else:
            return jsonify(response), 200

    @classmethod
    def get_user(cls, user_id):
        if session["user_id"] == user_id:
            if not User.exist(user_id):
                raise NotFound(user_id, "user")

            user = User.get_user(user_id)
            return jsonify(user.serialize()), 200
        else:
            raise ForbiddenAction()

    @classmethod
    def delete_user(cls, user_id):
        if not User.exist(user_id):
            raise NotFound(user_id, "user")

        if session["user_id"] == user_id:
            User.delete_user(user_id)
            return jsonify({"message": "User deleted successfully"}), 204
        else:
            raise ForbiddenAction()

    @classmethod
    def update_user(cls, user_id):
        if not User.exist(user_id):
            raise NotFound(user_id, "user")

        if session["user_id"] == user_id:
            update_data = request.json
            og_user = User.get_user(user_id)
            image_path = og_user.image
            
            if 'image' in update_data:
                base64_image_data = update_data['image']
                image_data = base64.b64decode(base64_image_data.split(',')[1])
                filename = f'{og_user.username}_av.jpg'
                image_path = os.path.join(Config.UPLOAD_FOLDER, filename)
                with open(image_path, 'wb') as f:
                    f.write(image_data)

            User.update_user(
                (
                    update_data.get("username", og_user.username),
                    image_path,
                    user_id,
                )
            )
            return jsonify({"message": "User updated successfully"}), 200
        else:
            raise ForbiddenAction()
    
    @classmethod
    def add_user_to_server(cls):
        user_id = session["user_id"]
        server_id = request.args.get("server_id", None)
        if server_id == None:
            server_id = Server.get_last_server_created()
        User.add_user_to_server((user_id, server_id))
        return jsonify({"message": "User added"}), 201
    
    @classmethod
    def get_user_servers(cls):
        """Get Servers an User is in"""
        user_id = session["user_id"]
        servers = Server.get_user_servers((user_id,))
        response = {"servers": [], "total": 0}

        if servers:
            servers_list = []
            for server in servers:
                servers_list.append(server.serialize())

            response["servers"] = servers_list
            response["total"] = len(servers_list)
            return jsonify(response), 200

        return jsonify(response), 200
    