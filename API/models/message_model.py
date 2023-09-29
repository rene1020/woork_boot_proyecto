from ..data_base import DatabaseConnection
from ..models.exceptions import InvalidDataError

class Message:
    def __init__(self, **kwargs) -> None:
        self.message_id = kwargs.get('message_id', None)
        self.message_body = kwargs.get('message_body', None)
        self.user_id = kwargs.get('user_id', None)
        self.channel_id = kwargs.get('channel_id', None)
        self.creation_date = kwargs.get('creation_date', None)
        self.update_date = kwargs.get('update_date', None)
        self.username = kwargs.get('username', None)
        
    @classmethod
    def get_message(cls, msg_id):
        query = "SELECT * FROM messages WHERE message_id = %s"
        msg = DatabaseConnection.fetch_one(query, (msg_id,))
        if msg is not None:
            return Message(
                message_id = msg[0],
                message_body = msg[1],
                user_id = msg[2],
                channel_id = msg[3],
                creation_date = msg[4],
                update_date = msg[5]
            )
        return None

    @classmethod
    def get_messages(cls, channel_id) -> list['Message']:
        query = "SELECT messages.message_id, messages.message_body, messages.user_id, messages.channel_id, messages.creation_date, messages.update_date, users.username FROM messages JOIN users ON messages.user_id = users.user_id WHERE channel_id = %s"
        msgs = DatabaseConnection.fetch_all(query, (channel_id,))
        
        msg_list = []
        for msg in msgs:
            msg_data = Message(
                message_id = msg[0],
                message_body = msg[1],
                user_id = msg[2],
                channel_id = msg[3],
                creation_date = msg[4],
                update_date = msg[5],
                username = msg[6]
            )
            msg_list.append(msg_data)
        
        return msg_list
    
    @classmethod
    def delete_message(cls, message_id) -> None:
        query = "DELETE FROM messages WHERE message_id = %s"
        DatabaseConnection.execute_query(query, (message_id,))

    @classmethod
    def create_message(cls, message: 'Message') -> None:
        query = "INSERT INTO messages (message_body, user_id, channel_id) VALUES (%s, %s, %s)"
        params = (message.message_body, message.user_id, message.channel_id)
        DatabaseConnection.execute_query(query, params)
    
    @classmethod
    def update_message(cls, params: tuple) -> None:
        query = "UPDATE messages SET message_body = %s, update_date = CURRENT_TIMESTAMP() WHERE message_id = %s"
        DatabaseConnection.execute_query(query, params)

    @classmethod
    def exist(cls, msg_id: int):
        query = "SELECT 1 FROM messages WHERE message_id = %s"
        result = DatabaseConnection.fetch_one(query, (msg_id,))
        return result is not None
        
    @classmethod
    def validate_data(cls, data) -> 'Message':
        """Validate message data"""
        msg_body = data[0]
        if len(msg_body) < 1:
            raise InvalidDataError("Message Body must have at least one character")

        msg_user_id = data[1]
        if not isinstance(msg_user_id, int):
            raise InvalidDataError("User Id must be a integer")

        msg_channel_id = data[2]
        if not isinstance(msg_channel_id, int):
            raise InvalidDataError("Channel Id must be a integer")
        
        return Message(message_body = msg_body, user_id = msg_user_id, channel_id = msg_channel_id)

    def serialize(self):
        return {
            'message_id': self.message_id,
            'message_body': self.message_body,
            'user_id': self.user_id,
            'channel_id': self.channel_id,
            'creation_date': self.creation_date,
            'update_date': self.update_date,
            'username': self.username
        }