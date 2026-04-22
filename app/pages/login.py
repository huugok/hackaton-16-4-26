import streamlit as st
import os
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

def login():
    st.title("🔐 Login")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        try:
            response = requests.post(
                f"{API_URL}/login", 
                json={"username": username, "password": password},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.logged_in = True
                st.session_state.username = data.get("username", username)
                st.success("Login correcto")
                st.rerun()
            else:
                try:
                    error_msg = response.json().get("detail", "Usuario o contraseña incorrectos")
                except:
                    error_msg = "Usuario o contraseña incorrectos"
                st.error(error_msg)
        except requests.exceptions.RequestException:
            st.error("Error al conectar con el servidor (API).")

def main_app():
    st.set_page_config(initial_sidebar_state="collapsed")
    st.title(f"Bienvenido {st.session_state.username} 👋")

    if st.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

    st.write("Aquí va tu app (dashboard, modelo IA, etc.)")

if st.session_state.logged_in:
    main_app()
else:
    login()