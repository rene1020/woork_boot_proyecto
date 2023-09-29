"""Channel Model"""

from ..data_base import DatabaseConnection
from ..models.exceptions import InvalidDataError


class Channel:
    """Class Channel"""

    def __init__(self, **kwargs):
        self.id_canal = kwargs.get("id_canal", None)
        self.nombre = kwargs.get("nombre", None)
        self.id_server = kwargs.get("id_server", None)
        self.id_usuario = kwargs.get("id_usuario", None)

    @classmethod
    def create_channel(cls, channel):
        """Create channel"""
        query = "INSERT INTO chanal (nombre, id_Server, id_usuario) VALUES (%s, %s, %s)"
        params = (channel.channel_name, channel.server_id, channel.user_id)
        DatabaseConnection.execute_query(query, params)

    @classmethod
    def update_channel(cls, channel_id, params):
        """Update channel"""
        query = "UPDATE chanal SET nombre = %s WHERE id_canal = %s"
        DatabaseConnection.execute_query(
            query, (params.get("nombre"), channel_id)
        )

    @classmethod
    def get_channels(cls, server_id=None):
        """Get channels"""
        if server_id:
            query = """
                SELECT id_canal, nombre, id_server, id_usuario
                FROM chanal
                WHERE id_server = %s
            """
            params = (server_id,)
        else:
            query = """
                SELECT id_canal, nombre, id_server, id_usuario
                FROM canal
            """
            params = ()

        channels = DatabaseConnection.fetch_all(query, params)

        channels_list = []
        for channel in channels:
            channel_data = Channel(
                channel_id=channel[0],
                channel_name=channel[1],
                server_id=channel[2],
                user_id=channel[3],
            )
            channels_list.append(channel_data)

        return channels_list

    @classmethod
    def get_channel(cls, channel_id):
        """Get channel"""
        query = """
            SELECT c.channel_id, c.channel_name, c.server_id, s.server_name, c.user_id, u.username
            FROM channels c
            INNER JOIN servers s ON c.server_id = s.server_id
            INNER JOIN users u ON c.user_id = u.user_id
            WHERE c.channel_id = %s
        """
        channel_data = DatabaseConnection.fetch_one(query, (channel_id,))
        if channel_data is not None:
            channel = Channel(
                channel_id=channel_data[0],
                channel_name=channel_data[1],
                server_id=channel_data[2],
                server_name=channel_data[3],
                user_id=channel_data[4],
                username=channel_data[5],
            )
            return channel

        return None

    @classmethod
    def delete_channel(cls, channel_id):
        """Delete channel"""
        query = "DELETE FROM canal WHERE id_canal = %s"
        DatabaseConnection.execute_query(query, (channel_id,))

    @classmethod
    def validate_data(cls, data):
        """Validate data"""
        channel_name = data.get("nombre", None)
        server_id = data.get("id_server", None)
        user_id = data.get("id_server", None)

        if not channel_name or len(channel_name) < 1:
            raise InvalidDataError("Channel name must not be empty")

        if not server_id:
            raise InvalidDataError("Server ID must not be empty")

        if not user_id:
            raise InvalidDataError("User ID must not be empty")

        return Channel(
            channel_name=channel_name,
            server_id=server_id,
            user_id=user_id,
        )

    @classmethod
    def exists(cls, channel_id):
        """Exists"""
        query = "SELECT 1 FROM canal WHERE id_canal= %s"
        result = DatabaseConnection.fetch_one(query, (channel_id,))
        return result is not None

    @classmethod
    def exists_by_name(cls, channel_name):
        """Check exists channel name"""
        query = "SELECT 1 FROM canal WHERE nombre = %s"
        result = DatabaseConnection.fetch_one(query, (channel_name,))
        return result is not None
