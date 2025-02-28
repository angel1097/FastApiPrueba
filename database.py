import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus

from urllib.parse import quote

#password = quote("Nb@N91*5")


URL_DATABASE = "mysql+pymysql://root:uwJeOkWbnjscRSEhZlacEeUNNygfcsQZ@shinkansen.proxy.rlwy.net:26710/railway"

#URL_DATABASE = f"mysql+pymysql://u954703204_tortillita:{password}@srv867.hstgr.io/u954703204_TortilleriaSys"

engine= create_engine(URL_DATABASE)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()
try:
    # Probar conexión
    with engine.connect() as connection:
        print("Conexión exitosa a la base de datos")
except Exception as e:
    print(f"Error de conexión: {e}")