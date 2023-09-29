from flask import jsonify

class CustomException(Exception):
    def __init__(self, status_code, name="Error", description = "Error") -> None:
        super().__init__(description)
        self.status_code = status_code
        self.name = name
    
    def get_response(self):
        response = jsonify({
            'error': {
                'code': self.status_code,
                'name': self.name,
                'description': self.description,
            }
        })
        response.status_code = self.status_code
        return response

class InvalidDataError(CustomException):
    def __init__(self, name="Invalid Data", description="Invalid data provided"):
        super().__init__(400, name, description)
        self.description = description
        self.status_code = 400
        self.name = name

class NameConflictError(CustomException):
    def __init__(self, model: str, attribute: str , value:str):
        name = f"{model.capitalize()} Conflict Error"
        description = f"{attribute.capitalize()} {value} is already taken"
        super().__init__(409, name, description)
        self.description = description
        self.status_code = 409
        self.name = name
        
class NotFound(CustomException):
    def __init__(self, id: int, model: str):
        name = f"{model.capitalize()} Not Found"
        description = f"{model.capitalize()} with id {id} not found"
        super().__init__(404, name, description)
        self.description = description
        self.status_code = 404
        self.name = name
        
class UnauthorizedAccess(CustomException):
    def __init__(self, name="Unauthorized Access", description="Login required"):
        super().__init__(401, name, description)
        self.description = description
        self.status_code = 401
        self.name = name
        
class ForbiddenAction(CustomException):
    def __init__(self, name="Forbidden Action", description="You can't perform this action."):
        super().__init__(401, name, description)
        self.description = description
        self.status_code = 401
        self.name = name
        
class ServerError(CustomException):
    def __init__(self, name="Internal Server Error", description="Internal Server Error"):
        super().__init__(500, name, description)
        self.description = description
        self.status_code = 500
        self.name = name
        