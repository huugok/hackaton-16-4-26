import streamlit as st
import os
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Registro de Usuario", page_icon="📝")

st.title("📝 Crear Cuenta")
st.markdown("Por favor, completa los siguientes campos para registrarte.")

# Usamos un formulario para agrupar los inputs y validarlos juntos al enviar
with st.form("registro_form", clear_on_submit=True):
    new_user = st.text_input("Nombre de Usuario", placeholder="Ingresa tu nombre de usuario")
    new_email = st.text_input("Correo Electrónico", placeholder="ejemplo@correo.com")
    new_password = st.text_input("Contraseña", type="password", placeholder="Ingresa una contraseña segura")
    confirm_password = st.text_input("Confirmar Contraseña", type="password", placeholder="Repite tu contraseña")
    
    submit_button = st.form_submit_button("Registrarse")

    if submit_button:
        # Validaciones básicas
        if not new_user or not new_email or not new_password or not confirm_password:
            st.error("⚠️ Todos los campos son obligatorios.")
        elif new_password != confirm_password:
            st.error("⚠️ Las contraseñas no coinciden.")
        elif len(new_password) < 6:
            st.warning("⚠️ La contraseña debe tener al menos 6 caracteres.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/register",
                    json={
                        "username": new_user,
                        "email": new_email,
                        "password": new_password
                    },
                    timeout=5
                )
                
                if response.status_code == 200:
                    st.success(f"✅ ¡Cuenta creada exitosamente para el usuario **{new_user}**!")
                    st.info("Ya puedes navegar a la página de Login desde el menú lateral para iniciar sesión.")
                else:
                    try:
                        error_msg = response.json().get("detail", "Error al registrar el usuario")
                    except:
                        error_msg = "Error al registrar el usuario"
                    st.error(f"⚠️ {error_msg}")
            except requests.exceptions.RequestException:
                st.error("Error al conectar con el servidor (API).")
