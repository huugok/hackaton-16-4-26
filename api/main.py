from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import joblib

model = joblib.load("model/model.pkl")


app = FastAPI()

@app.get("/")
def inicio():
    return {"mensaje": "API funcionando"}


class InputTexto(BaseModel):
    texto: str

@app.post("/predict")
def predict(data: InputTexto):

    print(data.texto) 
    texto_usuario = data.texto
   
    #aqui hay que llamar al modelo de ia 

    if #respuesta del modelo == 1:
        resultado = "Busca ayuda profesional"  
    elif #respuesta del modelo == 0:
        resultado = "estás bien, pero sigue cuidando tu salud mental"
   
    
    return {"prediccion": resultado}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)