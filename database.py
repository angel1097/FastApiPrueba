import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus


#URL_DATABASE = "mysql+pymysql://u9547:yvgaFYLdXaFEmnvLVCKTglnvXRUKPzNl@monorail.proxy.rlwy.net:14199/railway"
# Escapar la contraseña para evitar problemas con caracteres especiales

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

    
#password = quote_plus("Nb@N91*5")

# Obtener la contraseña de una variable de entorno
#password = quote_plus(os.getenv("DB_PASSWORD", "Nb@N91*5"))

#URL_DATABASE = f"mysql+pymysql://u954703204_tortillita:{password}@srv867.hstgr.io:3306/u954703204_TortilleriaSys"

#engine = create_engine(URL_DATABASE)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Base = declarative_base()

#try:
 #   with engine.connect() as connection:
  #      print("✅ Conexión exitosa a la base de datos")
#except Exception as e:
 #   print(f"❌ Error de conexión: {e}")