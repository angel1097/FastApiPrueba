from fastapi import FastAPI, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session 
import models, schemas
import auth
from database import SessionLocal

app = FastAPI(
    title="API de Gestión", 
    description="API para gestionar registros, autenticación, proveedores y futuras implementaciones de pedidos y facturas.",
    version="1.0",
    openapi_tags=[
        {"name": "General", "description": "Rutas generales de la API"},
        {"name": "Autenticación", "description": "Rutas relacionadas con login y autenticación"},
        {"name": "Proveedores", "description": "Manejo de proveedores en el sistema"},
        {"name": "Pedidos", "description": "Endpoints para la gestión de pedidos (Futuro)"},
        {"name": "Facturas", "description": "Endpoints para la gestión de facturas (Futuro)"}
    ]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(UserLogin):
    pass

# Dependencia para obtener la sesión de la BD
@app.get("/",dependencies=[Depends(auth.get_current_user)], tags=["General"])
async def root():
    return {"message": "Bienvenido a la API de registros"}

@app.post("/register/", dependencies=[Depends(auth.get_current_user)],tags=["Autenticación"])
async def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    hashed_password = models.User.hash_password(user_data.password)
    new_user = models.User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role  # Guardamos el rol del usuario
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "Usuario registrado exitosamente"}

@app.post("/token/", tags=["Autenticación"])
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if not user or not user.verify_password(user_data.password):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/registro/", response_model=schemas.IngresoResponse, dependencies=[Depends(auth.get_current_user)], tags=["General"])
def crear_ingreso(ingreso: schemas.IngresoCreate, db: Session = Depends(get_db)):
    nuevo_ingreso = models.Ingreso(**ingreso.dict())
    db.add(nuevo_ingreso)
    db.commit()
    db.refresh(nuevo_ingreso)
    return nuevo_ingreso

@app.get("/listarregistros/", dependencies=[Depends(auth.get_current_user)], tags=["General"])
async def consultar_registros(db: Session = Depends(get_db)):
    registros = db.query(models.Ingreso).all()
    return registros

@app.post("/proveedores/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProveedorResponse, dependencies=[Depends(auth.get_current_user)], tags=["Proveedores"])
async def crear_proveedor(proveedor: schemas.ProveedorBase, db: Session = Depends(get_db)):
    nuevo_proveedor = models.Proveedor(**proveedor.dict())
    db.add(nuevo_proveedor)
    db.commit()
    db.refresh(nuevo_proveedor)
    return nuevo_proveedor

@app.get("/proveedores/", status_code=status.HTTP_200_OK, response_model=list[schemas.ProveedorResponse], dependencies=[Depends(auth.get_current_user)], tags=["Proveedores"])
async def listar_proveedores(db: Session = Depends(get_db)):
    proveedores = db.query(models.Proveedor).all()
    return proveedores

@app.get("/proveedores/{id_proveedor}", status_code=status.HTTP_200_OK, response_model=schemas.ProveedorResponse, dependencies=[Depends(auth.get_current_user)], tags=["Proveedores"])
async def obtener_proveedor(id_proveedor: int, db: Session = Depends(get_db)):
    proveedor = db.query(models.Proveedor).filter(models.Proveedor.id_proveedor == id_proveedor).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor

@app.put("/proveedores/{id_proveedor}", status_code=status.HTTP_200_OK, response_model=schemas.ProveedorResponse, dependencies=[Depends(auth.get_current_user)], tags=["Proveedores"])
async def actualizar_proveedor(id_proveedor: int, proveedor: schemas.ProveedorBase, db: Session = Depends(get_db)):
    proveedor_db = db.query(models.Proveedor).filter(models.Proveedor.id_proveedor == id_proveedor).first()
    if not proveedor_db:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    for key, value in proveedor.dict(exclude_unset=True).items():
        setattr(proveedor_db, key, value)
    db.commit()
    db.refresh(proveedor_db)
    return proveedor_db

@app.delete("/proveedores/{id_proveedor}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(auth.get_current_user)], tags=["Proveedores"])
async def eliminar_proveedor(id_proveedor: int, db: Session = Depends(get_db)):
    proveedor = db.query(models.Proveedor).filter(models.Proveedor.id_proveedor == id_proveedor).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    db.delete(proveedor)
    db.commit()
    return {"message": "Proveedor eliminado exitosamente"}

# Endpoints para futuras implementaciones
