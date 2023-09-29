"""Server Controller"""

from flask import request, jsonify, session
from ..models.server_model import Server
from ..models.user_model import User
from ..models.exceptions import NotFound, ForbiddenAction, ServerError


class ServerController:
    """Class Server Controller"""

    @classmethod
    def create_server(cls):
        """Create Server"""
        server_data = request.json
        owner_id = session["user_id"]

        if Server.exists_by_name(server_data.get("server_name")):
            return jsonify({"message": "Server with this name already exists"}), 400

        server = Server.validate_data(
            {
                "server_name": server_data.get("server_name"),
                "server_description": server_data.get("server_description"),
                "owner_id": owner_id,
            }
        )

        Server.create_server(server)

        server_id = Server.get_last_server_created()

        if server_id == None:
            raise ServerError()

        User.add_user_to_server((owner_id, server_id,))
        return jsonify({"message": "Server created successfully"}), 201

    @classmethod
    def get_servers(cls):
        """Get Servers"""
        server_name = request.args.get("server_name")
        servers = Server.get_servers(server_name)
        response = {"servers": [], "total": 0}

        if servers:
            servers_list = []
            for server in servers:
                server_dict = {
                    "server_id": server.server_id,
                    "server_name": server.server_name,
                    "server_description": server.server_description,
                    "owner_id": server.owner_id,
                    "owner_username": server.owner_username,
                    "members": server.members,
                }
                servers_list.append(server_dict)

            response["servers"] = servers_list
            response["total"] = len(servers_list)
            return jsonify(response), 200

        return jsonify(response), 200

    @classmethod
    def get_server(cls, server_id):
        """Get Server"""
        server = Server.get_server(server_id)
        if server:
            server_dict = {
                "server_id": server.server_id,
                "server_name": server.server_name,
                "server_description": server.server_description,
                "owner_id": server.owner_id,
            }
            return jsonify(server_dict), 200

        raise NotFound(server_id, "server")

    @classmethod
    def update_server(cls, server_id):
        """Update Server"""
        update_data = request.json
        updated_fields = {}

        if "server_name" in update_data:
            new_server_name = update_data["server_name"]
            if Server.exists_by_name(new_server_name):
                return jsonify({"message": "Server with this name already exists"}), 400

            if len(new_server_name) < 5:
                return (
                    jsonify({"message": "Server name must have at least 5 characters"}),
                    400,
                )

            updated_fields["server_name"] = new_server_name

        if "server_description" in update_data:
            updated_fields["server_description"] = update_data["server_description"]

        if updated_fields:
            if not Server.exist(server_id):
                raise NotFound(server_id, "server")

            server = Server.get_server(server_id)
            if server.owner_id != session["user_id"]:
                raise ForbiddenAction()

            Server.update_server(server_id, updated_fields)
            return jsonify({"message": "Server updated successfully"}), 200

        return jsonify({"message": "No valid fields to update"}), 400

    @classmethod
    def delete_server(cls, server_id):
        """Delete Server"""
        if not Server.exist(server_id):
            raise NotFound(server_id, "server")

        server = Server.get_server(server_id)
        if server.owner_id != session["user_id"]:
            raise ForbiddenAction()

        Server.delete_server(server_id)
        return jsonify({"message": "Server deleted successfully"}), 204
