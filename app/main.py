#import pandas as pd
#from sklearn.linear_model import LinearRegression
import streamlit as st
import requests
import time
import json
import os


API_URL = os.getenv("API_URL", "http://localhost:5000")

print("Entorno configurado correctamente")

#model = LinearRegression()
#print("Model initialized")

st.set_page_config(
    page_title="MindCheck",
    page_icon="🧠",
    layout="centered",
)


st.title("MindCheck - Predicción de Ansiedad")


# ── Formulario ────────────────────────────────────────────────────────────────
texto_usuario = st.text_area(
    label="Tu texto",
    placeholder="Escribe aquí cómo te has sentido últimamente...",
    height=180,
    max_chars=1000,
    label_visibility="collapsed",
)

# Contador de caracteres
chars = len(texto_usuario)
st.markdown(f"<div class='char-counter'>{chars} / 1000</div>", unsafe_allow_html=True)



#bloque de codigo donde se cree un objeto json con el texto del usuario y se envie a la api de flask para obtener la prediccion de ansiedad y mostrarla en pantalla
if st.button("Analizar"):
    data = {"texto": texto_usuario}
    try:
        with st.spinner('Analizando el texto...'):  
            response =requests.post(f"{API_URL}/predict", json=data, timeout=10)
            if response.status_code == 200:
                prediccion = response.json().get("prediccion", "Desconocida")
                st.markdown(f"### Predicción de Ansiedad: {prediccion}")
            else:
                st.error(f"Error en la API. Código de estado: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error("No se pudo conectar con la API de predicción. Asegúrate de que Flask esté corriendo.")




