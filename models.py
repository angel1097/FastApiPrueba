from sqlalchemy import String, Integer, Column
from database import Base
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)
    
    def verify_password(self, password: str):
        return pwd_context.verify(password, self.hashed_password)
    
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

class Ingreso(Base):
    __tablename__ = "ingresos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    descripcion = Column(String(255), nullable=False)
    cantidad = Column(Integer, nullable=False)
    
class Proveedor(Base):
    __tablename__ = "proveedores"
    id_proveedor = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_proveedor = Column(String(100), nullable=False)
    rfc = Column(String(13))
    direccion = Column(String(50))
    telefono = Column(String(20))
    email = Column(String(100))
    contacto = Column(String(50))
    producto_principal = Column(String(50))
