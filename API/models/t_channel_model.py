from ..data_base import DatabaseConnection

class Channel:
    def __init__(self, **kwargs):
        self.channel_id = kwargs.get("id_canal", None)
        self.channel_name = kwargs.get("nombre", None)
        self.user_id = kwargs.get("id_usuario", None)
        self.server_id = kwargs.get("id_servidor", None)
    
    @classmethod
    def create_channel(cls, channel: 'Channel'):
        query = "INSERT INTO canal (nombre, id_usuario, id_servidor) VALUES (%s, %s, %s)"
        params = (channel.channel_name, channel.user_id, channel.server_id)
        DatabaseConnection.execute_query(query, params)
        
    @classmethod
    def get_channels_from_server(cls, server_id) -> list['Channel']:
        query = "SELECT id_canal, nombre, id_usuario, id_servidor FROM canal WHERE server_id = %s"
        channels = DatabaseConnection.fetch_all(query, (server_id,))
        
        channels_list = []
        for channel in channels:
            ch_data = Channel(
                channel_id = channel[0],
                channel_name = channel[1],
                user_id = channel[2],
                server_id = channel[3],
            )
            channels_list.append(ch_data)
        
        return channels_list
        
    @classmethod
    def exists_name(cls, channel_name):
        """Comprobar si existe el servidor"""
        query = "SELECT 1 FROM chanal WHERE nombre = %s"
        result = DatabaseConnection.fetch_one(query, (channel_name,))
        return result is not None
    
    def serialize(self):
        return {
            "id_canal": self.channel_id,
            "nombre": self.channel_name,
            "id_usuario": self.user_id,
            "id_server": self.server_id
        }