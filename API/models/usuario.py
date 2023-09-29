from API.data_base import DatabaseConnection
class Usuario:
    _keys = ["id_usuario", "nombre_usuario", "password", "perfil_imagen"]
    def __init__(self, **kwargs):
        self.id_usuario = kwargs.get("id_usuario")
        self.nombre_usuario = kwargs.get("nombre_usuario")
        self.password = kwargs.get("password")
        self.email = kwargs.get("email")
        self.perfil_imagen = kwargs.get("perfil_imagen")
        
        
    def serialize(self):
        return {
            "id_usuario": self.id_usuario,
            "nombre_usuario": self.nombre_usuario,
            "password": self.password,
            "perfil_imagen": self.perfil_imagen,
        }
    
    @classmethod
    def crear_usuario(self,usuario):
        query="Insert into usuarios(nombre_usuario, password, email, pefil_imagen) values (%s,%s,%s,%s)"
        parametros=(usuario.nombre_usuario,usuario.password,usuario.email,usuario.perfil_imagen,)
        DatabaseConnection.execute_query(query,parametros)
        DatabaseConnection.close_connection()
        
    @classmethod
    def buscar_usuario(self,usuario):
        query="select * from usuarios where id_usuario=%s"
        parametros=(usuario.id_usuario,)
        usuario_encontrado=DatabaseConnection.fetch_one(query,parametros)
        if usuario_encontrado : 
            return Usuario(id_usuario=usuario_encontrado[0],
                        nombre_usuario=usuario_encontrado[1],
                        password=usuario_encontrado[2],
                        email=usuario_encontrado[3],
                        perfil_imagen=usuario_encontrado[4]
                        )
        return None
    @classmethod
    def actualizar_usuario(self,usuario):
        query="update usuarios set nombre_usuario=%s, password=%s, email=%s, pefil_imagen=%s where id_usuario=%s"
        parametros=(usuario.nombre_usuario, usuario.password, usuario.email, usuario.perfil_imagen, usuario.id_usuario,)
        DatabaseConnection.execute_query(query,parametros)
    
    @classmethod
    def delete_user(cls, id_usuario: int):
        query = "DELETE FROM userarios WHERE user_id = %s"
        DatabaseConnection.execute_query(query, (id_usuario,))
    
            
        