from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = "mysql+pymysql://root:yvgaFYLdXaFEmnvLVCKTglnvXRUKPzNl@monorail.proxy.rlwy.net:14199/railway"
engine= create_engine(URL_DATABASE)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()
try:
    # Probar conexión
    with engine.connect() as connection:
        print("Conexión exitosa a la base de datos")
except Exception as e:
    print(f"Error de conexión: {e}")
