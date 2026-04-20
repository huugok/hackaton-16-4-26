import streamlit as st
import requests
import time

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="MindCheck",
    page_icon="🧠",
    layout="centered",
)

# ── CSS personalizado ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');

/* Variables */
:root {
    --bg: #F7F4EF;
    --surface: #FFFFFF;
    --text: #1A1A1A;
    --muted: #7A7570;
    --accent: #2D6A4F;
    --accent-light: #E8F4F0;
    --danger: #C0392B;
    --danger-light: #FDECEA;
    --border: #E2DDD8;
    --radius: 16px;
}

/* Fondo general */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding: 3rem 1.5rem 4rem !important; max-width: 700px !important; }

/* Tipografía */
h1, h2, h3 { font-family: 'DM Serif Display', serif !important; }

/* Textarea */
textarea {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    color: var(--text) !important;
    resize: none !important;
    padding: 1rem !important;
    transition: border-color 0.2s ease !important;
}
textarea:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(45,106,79,0.1) !important; }

/* Botón principal */
[data-testid="stButton"] > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.75rem 2.5rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
[data-testid="stButton"] > button:hover {
    background: #235c40 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(45,106,79,0.25) !important;
}

/* Cards de resultado */
.result-ok {
    background: var(--accent-light);
    border: 1.5px solid #b7dece;
    border-left: 5px solid var(--accent);
    border-radius: var(--radius);
    padding: 1.5rem 1.75rem;
    margin-top: 1.5rem;
}
.result-alert {
    background: var(--danger-light);
    border: 1.5px solid #f0b8b3;
    border-left: 5px solid var(--danger);
    border-radius: var(--radius);
    padding: 1.5rem 1.75rem;
    margin-top: 1.5rem;
}
.result-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    margin-bottom: 0.4rem;
}
.result-ok .result-title { color: var(--accent); }
.result-alert .result-title { color: var(--danger); }
.result-body {
    color: var(--text);
    font-size: 0.95rem;
    line-height: 1.6;
    font-weight: 300;
}
.resources {
    margin-top: 0.9rem;
    padding-top: 0.9rem;
    border-top: 1px solid #f0b8b3;
    font-size: 0.88rem;
    color: var(--muted);
}

/* Divisor */
hr { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }

/* Contador de caracteres */
.char-counter {
    text-align: right;
    font-size: 0.8rem;
    color: var(--muted);
    margin-top: -0.5rem;
    margin-bottom: 0.75rem;
}

/* Disclaimer */
.disclaimer {
    background: #F0EDE8;
    border-radius: 12px;
    padding: 0.9rem 1.2rem;
    font-size: 0.82rem;
    color: var(--muted);
    line-height: 1.5;
    margin-top: 2.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Cabecera ─────────────────────────────────────────────────────────────────
st.markdown("## 🧠 MindCheck")
st.markdown(
    "<p style='color:#7A7570; font-size:1rem; margin-top:-0.5rem; margin-bottom:2rem;'>"
    "Cuéntanos cómo te sientes. Nuestro sistema analizará tu texto de forma anónima."
    "</p>",
    unsafe_allow_html=True,
)

# ── Formulario ────────────────────────────────────────────────────────────────
texto = st.text_area(
    label="Tu texto",
    placeholder="Escribe aquí cómo te has sentido últimamente...",
    height=180,
    max_chars=1000,
    label_visibility="collapsed",
)

# Contador de caracteres
chars = len(texto)
st.markdown(f"<div class='char-counter'>{chars} / 1000</div>", unsafe_allow_html=True)

analizar = st.button("Analizar mi texto →", use_container_width=True)

# ── Lógica de predicción ──────────────────────────────────────────────────────
API_URL = "http://localhost:8000/predict"  # Cambia si tu API está en otro puerto

if analizar:
    if not texto.strip():
        st.warning("Por favor, escribe algo antes de analizar.")
    elif len(texto.strip()) < 20:
        st.warning("Escribe un poco más para que el análisis sea preciso (mínimo 20 caracteres).")
    else:
        with st.spinner("Analizando..."):
            try:
                response = requests.post(API_URL, json={"texto": texto}, timeout=10)
                response.raise_for_status()
                resultado = response.json()
                necesita_ayuda = resultado.get("necesita_ayuda", False)
                confianza = resultado.get("confianza", None)  # opcional, si tu API lo devuelve

            except requests.exceptions.ConnectionError:
                # ── MODO DEMO (sin API) ──────────────────────────────────────
                # Elimina este bloque cuando la API esté lista
                st.info("⚠️ API no conectada — mostrando resultado de demostración.")
                palabras_alerta = ["triste", "solo", "sola", "no puedo", "ayuda", "mal", "ansiedad", "miedo", "llorar"]
                necesita_ayuda = any(p in texto.lower() for p in palabras_alerta)
                confianza = None

            except Exception as e:
                st.error(f"Error al conectar con la API: {e}")
                st.stop()

        # ── Resultado ─────────────────────────────────────────────────────────
        if necesita_ayuda:
            confianza_texto = f" (confianza: {confianza:.0%})" if confianza else ""
            st.markdown(f"""
            <div class="result-alert">
                <div class="result-title">⚠️ Recomendamos apoyo profesional{confianza_texto}</div>
                <div class="result-body">
                    Lo que describes sugiere que podrías beneficiarte de hablar con un profesional de salud mental.
                    No estás solo/a y pedir ayuda es un acto de valentía.
                </div>
                <div class="resources">
                    📞 <strong>Teléfono de la Esperanza:</strong> 717 003 717 &nbsp;|&nbsp;
                    📞 <strong>Atención a conducta suicida:</strong> 024
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            confianza_texto = f" (confianza: {confianza:.0%})" if confianza else ""
            st.markdown(f"""
            <div class="result-ok">
                <div class="result-title">✅ Todo parece estar bien{confianza_texto}</div>
                <div class="result-body">
                    Tu texto no muestra señales de alerta significativas. Recuerda que cuidar
                    tu bienestar emocional de forma preventiva es igual de importante.
                    Si en algún momento lo necesitas, no dudes en buscar apoyo.
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── Separador y disclaimer ────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div class="disclaimer">
    🔒 <strong>Privacidad:</strong> Tu texto no se almacena ni se comparte. Este sistema
    es una herramienta de orientación y <strong>no sustituye el diagnóstico de un profesional de salud mental</strong>.
    Si estás en crisis, llama al <strong>024</strong>.
</div>
""", unsafe_allow_html=True)
