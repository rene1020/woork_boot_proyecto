from ..models.message_model import Message
from flask import request, jsonify, session
from ..models.exceptions import NotFound, ForbiddenAction

class MessageController:
    @classmethod
    def get_message(cls, message_id):
        if not Message.exist(message_id):
            raise NotFound(message_id, "message")

        msg = Message.get_message(message_id)
        return jsonify(msg.serialize()), 200

    @classmethod
    def get_messages(cls):
        channel_id = request.args.get('channel_id')
        msgs = Message.get_messages(channel_id)
        response = {}
        
        if msgs:
            msgs_list = []
            for msg in msgs:
                msgs_list.append(msg.serialize())
            
            response["messages"] = msgs_list
            response["total"] = len(msgs_list)
            return jsonify(response), 200
        else:
            return jsonify(response), 200
    
    @classmethod
    def delete_message(cls, message_id):
        if not Message.exist(message_id):
            raise NotFound(message_id, "message")
        
        msg = Message.get_message(message_id)
        
        if session['user_id'] == msg.user_id:
            Message.delete_message(message_id)
            return jsonify({'message': 'Message deleted successfully'}), 204
        else:
            raise ForbiddenAction()
        
    @classmethod
    def create_message(cls):
        msg_data = request.json

        new_msg = Message.validate_data([
            msg_data.get('message_body'),
            session['user_id'],
            msg_data.get('channel_id') 
        ])
        
        Message.create_message(new_msg)
        return jsonify({'message': 'Message created successfully'}), 201
    
    @classmethod
    def update_message(cls, message_id):
        if not Message.exist(message_id):
            raise NotFound(message_id, "message")
        
        og_msg = Message.get_message(message_id)
        
        if session['user_id'] == og_msg.user_id:
            update_data = request.json
            
            Message.update_message((
                update_data.get('message_body', og_msg.message_body),
                message_id
            ))
            return jsonify({'message': 'Message updated successfully'}), 200
        else:
            raise ForbiddenAction()