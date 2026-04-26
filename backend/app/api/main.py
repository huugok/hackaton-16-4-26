# api/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn
import sys
import os
 
# Añadimos la carpeta raíz del proyecto al path para poder importar /model/predict.py
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
 
# Importamos la config de base de datos y los modelos
from backend.app.api.database import SessionLocal, engine, Base
import backend.app.api.models as models
 
# Importamos la función de predicción real
from backend.app.services.predict import predict_risk
 
# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)
 
app = FastAPI()
 
# CORS: permite que el frontend (Streamlit) pueda llamar a la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
class InputTexto(BaseModel):
    texto: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

import hashlib
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
 
@app.get("/")
def inicio():
    return {"mensaje": "API MindCheck funcionando ✅"}

@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter((models.User.username == user.username) | (models.User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario o correo ya está registrado")
    
    hashed_pwd = hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, password_hash=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "Usuario registrado exitosamente", "username": db_user.username}

@app.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or db_user.password_hash != hash_password(user.password):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
        
    return {"message": "Login exitoso", "username": db_user.username}
 
@app.post("/predict")
def predict(data: InputTexto, db: Session = Depends(get_db)):
    try:
        texto_usuario = data.texto
 
        # Llamar al modelo de IA real (traduce al inglés internamente)
        probabilidad, nivel = predict_risk(texto_usuario)
        prediccion_numerica = round(probabilidad, 2)
 
        if nivel == "Alto":
            resultado = "Busca ayuda profesional"
        elif nivel == "Medio":
            resultado = "Presta atención a tu bienestar mental"
        else:
            resultado = "Estás bien, pero sigue cuidando tu salud mental"
 
        # Guardar en base de datos
        nuevo_registro = models.PredictionRecord(
            texto_usuario=texto_usuario,
            resultado_ia=int(probabilidad),
            mensaje_devuelto=resultado
        )
        db.add(nuevo_registro)
        db.commit()
        db.refresh(nuevo_registro)
 
        return {
            "prediccion": resultado,
            "nivel_riesgo": nivel,
            "probabilidad": prediccion_numerica,
            "id_registro": nuevo_registro.id
        }
 
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)