from sqlalchemy import String,Integer,Column
from database import Base

class Ingreso(Base):
    __tablename__="registrodeingreso"
    idregistro=Column(Integer,primary_key=True,index=True)
    documentoingreso=Column(String(100))
    nombrepersona=Column(String(100))

