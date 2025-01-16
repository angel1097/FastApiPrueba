from sqlalchemy import String,Integer,Column
from database import Base

class Ingreso(Base):
    __tablename__="registrodeingreso"
    idregistro=Column(Integer,primary_key=True,index=True)
    documentoingreso=Column(String(100))
    nombrepersona=Column(String(100))

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