import streamlit as st
import hashlib

##Para test
USERS = {
    "admin": "1234",
    "hugo": "password"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    st.title("🔐 Login")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login correcto")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

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