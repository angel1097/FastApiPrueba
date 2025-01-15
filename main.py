from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

class IngresoBase(BaseModel):
    documentoingreso: str
    nombrepersona: str

class IngresoBase2(BaseModel):
    idregistro: int
    documentoingreso: str
    nombrepersona: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de registros"}

@app.post("/registro/", status_code=status.HTTP_201_CREATED)
async def crear_registro(registro: IngresoBase, db: db_dependency):
    db_registro = models.Ingreso(**registro.dict())
    db.add(db_registro)
    db.commit()
    return {"message": "El registro se realizó exitosamente"}

@app.get("/listarregistros/", status_code=status.HTTP_200_OK)
async def consultar_registros(db: db_dependency):
    registros = db.query(models.Ingreso).all()
    return registros

@app.get("/consultaregistro/{documento_ingreso}", status_code=status.HTTP_200_OK)
async def consultar_registros_por_documento(documento_ingreso: str, db: db_dependency):
    registro = db.query(models.Ingreso).filter(models.Ingreso.documentoingreso == documento_ingreso).first()
    if registro is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro

@app.delete("/borrarregistro/{id_registro}", status_code=status.HTTP_200_OK)
async def borrar_registro(id_registro: int, db: db_dependency):
    registroborrar = db.query(models.Ingreso).filter(models.Ingreso.idregistro == id_registro).first()
    if registroborrar is None:
        raise HTTPException(status_code=404, detail="No se puede borrar, el registro no existe")
    db.delete(registroborrar)
    db.commit()
    return {"message": "El registro se eliminó exitosamente"}

@app.post("/actualizarregistro/", status_code=status.HTTP_200_OK)
async def actualizar_registro(registro: IngresoBase2, db: db_dependency):
    registroactualizar = db.query(models.Ingreso).filter(models.Ingreso.idregistro == registro.idregistro).first()
    if registroactualizar is None:
        raise HTTPException(status_code=404, detail="No se encuentra el registro")
    registroactualizar.documentoingreso = registro.documentoingreso
    registroactualizar.nombrepersona = registro.nombrepersona
    db.commit()
    return {"message": "Registro actualizado exitosamente"}
