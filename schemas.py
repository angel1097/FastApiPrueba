from pydantic import BaseModel, EmailStr
from datetime import datetime

class IngresoBase(BaseModel):
    usuario_id: int
    fecha_ingreso: datetime


class UserBase(BaseModel):
    username: str
    password: str
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
class IngresoCreate(IngresoBase):
    pass

class IngresoResponse(IngresoBase):
    id: int

    class Config:
        from_attributes = True
class ProveedorBase(BaseModel):
    nombre_proveedor: str
    rfc: str
    direccion: str
    telefono: str
    email: str
    contacto: str
    producto_principal: str

# ProveedorCreate hereda de ProveedorBase y se usa para la creación de proveedores
class ProveedorCreate(ProveedorBase):
    pass

# ProveedorResponse hereda de ProveedorBase y se usa para la respuesta de un proveedor
class ProveedorResponse(ProveedorBase):
    id_proveedor: int  # Este es el ID que asigna la base de datos

    class Config:
        from_attributes = True  # Para mapear automáticamente desde SQLAlchemy