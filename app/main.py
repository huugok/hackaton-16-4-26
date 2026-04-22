import streamlit as st
import requests
import os
 
API_URL = os.getenv("API_URL", "http://localhost:8000")
 
st.set_page_config(
    page_title="MindCheck",
    page_icon="🧠",
    layout="centered",
)
 
st.title("MindCheck - Predicción de Ansiedad")
 
texto_usuario = st.text_area(
    label="Tu texto",
    placeholder="Escribe aquí cómo te has sentido últimamente...",
    height=180,
    max_chars=1000,
    label_visibility="collapsed",
)
 
chars = len(texto_usuario)
st.markdown(f"<div class='char-counter'>{chars} / 1000</div>", unsafe_allow_html=True)
 
if st.button("Analizar"):
    if not texto_usuario.strip():
        st.warning("Por favor escribe algo antes de analizar.")
    else:
        data = {"texto": texto_usuario}
        try:
            with st.spinner("Analizando el texto..."):
                response = requests.post(f"{API_URL}/predict", json=data, timeout=30)
                if response.status_code == 200:
                    result = response.json()
                    prediccion = result.get("prediccion", "Desconocida")
                    nivel = result.get("nivel_riesgo", "")
                    prob = result.get("probabilidad", 0)
 
                    st.markdown(f"### 🧠 Resultado: {prediccion}")
                    st.markdown(f"**Nivel de riesgo:** {nivel}  |  **Probabilidad:** {prob:.1f}%")
 
                    # Barra de progreso visual
                    st.progress(int(prob))
                else:
                    st.error(f"Error en la API. Código de estado: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error("No se pudo conectar con la API. Asegúrate de que FastAPI esté corriendo en el puerto 8000.")
            st.info("Ejecuta en otra terminal: `cd api && uvicorn main:app --reload`")