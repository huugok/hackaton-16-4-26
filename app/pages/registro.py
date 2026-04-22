import streamlit as st
import hashlib

# Función de utilidad si en el futuro se desea integrar con la lógica de login
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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
            # TODO: Aquí iría la lógica para guardar en base de datos o archivo
            
            # Simulamos el registro exitoso
            st.success(f"✅ ¡Cuenta creada exitosamente para el usuario **{new_user}**!")
            st.info("Ya puedes navegar a la página de Login desde el menú lateral para iniciar sesión.")
