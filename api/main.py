from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import joblib

model = joblib.load("model/model.pkl")

texto_usuario : str
app = FastAPI()

@app.get("/")
def inicio():
    return {"mensaje": "API funcionando"}


class InputTexto(BaseModel):
    texto: str

@app.post("/predict")
def predict(data: InputTexto):
    try:
        print(data.texto) 
        texto_usuario = data.texto
    
        #aqui hay que llamar al modelo de ia 

        respuesta_modelo = model.predict([texto_usuario]) 

        if respuesta_modelo[0] == 1:
            resultado = "Busca ayuda profesional"  
        elif respuesta_modelo[0] == 0:
            resultado = "estás bien, pero sigue cuidando tu salud mental"
    
        
        return {"prediccion": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)