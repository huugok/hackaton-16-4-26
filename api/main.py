# api/main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn
import joblib

# Importamos la config de base de datos y los modelos
from api.database import SessionLocal, engine, Base
from api import models

# Crear las tablas en la base de datos (Equivalente al Update-Database de EF)
Base.metadata.create_all(bind=engine)

# Cargar modelo IA
#model = joblib.load("../model/model.pkl") 

app = FastAPI()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class InputTexto(BaseModel):
    texto: str

@app.get("/")
def inicio():
    return {"mensaje": "API funcionando"}

# Añadimos db: Session = Depends(get_db) para inyectar la base de datos
@app.post("/predict")
def predict(data: InputTexto, db: Session = Depends(get_db)):
    try:
        texto_usuario = data.texto
    
        # Llamar al modelo de IA
        #respuesta_modelo = model.predict([texto_usuario]) 
        #prediccion_numerica = int(respuesta_modelo[0])
        prediccion_numerica=1
        if prediccion_numerica == 1:
            resultado = "Busca ayuda profesional"  
        elif prediccion_numerica == 0:
            resultado = "Estás bien, pero sigue cuidando tu salud mental"
        else:
            resultado = "Resultado desconocido"

        # --- APLICAR LA IDEA DEL PROYECTO ISW: GUARDAR EN BASE DE DATOS ---
        # 1. Instanciar la entidad
        nuevo_registro = models.PredictionRecord(
            texto_usuario=texto_usuario,
            resultado_ia=prediccion_numerica,
            mensaje_devuelto=resultado
        )
        
        # 2. Añadir y guardar cambios (Equivalente a dbContext.Add() y dbContext.SaveChanges())
        db.add(nuevo_registro)
        db.commit()
        db.refresh(nuevo_registro) # Para obtener el ID autogenerado
        # ------------------------------------------------------------------
        
        return {"prediccion": resultado, "id_registro": nuevo_registro.id}
    
    except Exception as e:
        db.rollback() # Si hay un error, deshacemos los cambios
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)