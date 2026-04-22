import streamlit as st
import requests
import os
import random
from datetime import datetime, timedelta

API_URL = os.getenv("API_URL", "http://localhost:8000")

# ── Datos de demo (simulan BD) ─────────────────────────────────────────────────
PACIENTES_DEMO = {
    "Carlos M.": [
        {"fecha": datetime.now() - timedelta(days=6), "texto": "Hoy me ha costado levantarme, me siento muy agotado y sin motivación para nada.", "probabilidad": 72.3, "nivel": "Alto", "prediccion": "Busca ayuda profesional"},
        {"fecha": datetime.now() - timedelta(days=5), "texto": "Un poco mejor que ayer, pero sigo notando esa presión en el pecho cuando pienso en el trabajo.", "probabilidad": 58.1, "nivel": "Medio", "prediccion": "Presta atención a tu bienestar mental"},
        {"fecha": datetime.now() - timedelta(days=4), "texto": "Dormí mejor. Salí a caminar y eso me ayudó bastante.", "probabilidad": 34.7, "nivel": "Medio", "prediccion": "Presta atención a tu bienestar mental"},
        {"fecha": datetime.now() - timedelta(days=3), "texto": "Tuve una discusión fuerte en casa. Me siento solo y sin apoyo.", "probabilidad": 81.2, "nivel": "Alto", "prediccion": "Busca ayuda profesional"},
        {"fecha": datetime.now() - timedelta(days=2), "texto": "Sigo mal después de ayer. No tengo ganas de hablar con nadie.", "probabilidad": 79.5, "nivel": "Alto", "prediccion": "Busca ayuda profesional"},
        {"fecha": datetime.now() - timedelta(days=1), "texto": "Hablé con un amigo hoy. Me siento un poco más tranquilo.", "probabilidad": 52.0, "nivel": "Medio", "prediccion": "Presta atención a tu bienestar mental"},
        {"fecha": datetime.now(), "texto": "Día tranquilo, aunque aún pienso mucho en los problemas.", "probabilidad": 45.3, "nivel": "Medio", "prediccion": "Presta atención a tu bienestar mental"},
    ],
    "Laura G.": [
        {"fecha": datetime.now() - timedelta(days=6), "texto": "Me siento bien, aunque con algo de estrés por los exámenes.", "probabilidad": 28.4, "nivel": "Bajo", "prediccion": "Estás bien, pero sigue cuidando tu salud mental"},
        {"fecha": datetime.now() - timedelta(days=5), "texto": "Estudié mucho, estoy cansada pero contenta con mi progreso.", "probabilidad": 22.1, "nivel": "Bajo", "prediccion": "Estás bien, pero sigue cuidando tu salud mental"},
        {"fecha": datetime.now() - timedelta(days=4), "texto": "El examen fue difícil. Creo que no me ha salido bien y eso me angustia mucho.", "probabilidad": 61.8, "nivel": "Alto", "prediccion": "Busca ayuda profesional"},
        {"fecha": datetime.now() - timedelta(days=3), "texto": "Sigo preocupada por las notas. No puedo dejar de pensar en ello.", "probabilidad": 55.2, "nivel": "Medio", "prediccion": "Presta atención a tu bienestar mental"},
        {"fecha": datetime.now() - timedelta(days=2), "texto": "Me enteré que aprobé. Qué alivio tan grande, me siento mucho mejor.", "probabilidad": 19.3, "nivel": "Bajo", "prediccion": "Estás bien, pero sigue cuidando tu salud mental"},
        {"fecha": datetime.now() - timedelta(days=1), "texto": "Fin de semana relajado con la familia. Me siento muy bien.", "probabilidad": 12.7, "nivel": "Bajo", "prediccion": "Estás bien, pero sigue cuidando tu salud mental"},
        {"fecha": datetime.now(), "texto": "Todo bien hoy. Empiezo nueva semana con energía.", "probabilidad": 15.0, "nivel": "Bajo", "prediccion": "Estás bien, pero sigue cuidando tu salud mental"},
    ],
}

# ── Config ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MindCheck",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display:ital@0;1&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

section[data-testid="stSidebar"] {
    background: #0f1117;
    border-right: 1px solid #1e2130;
}
section[data-testid="stSidebar"] * { color: #e0e6f0 !important; }

.main { background: #f7f8fc; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

.mc-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
    margin-bottom: 1rem;
}
.mc-card-accent { border-left: 4px solid #5b6af0; }

.badge-alto { background:#fee2e2; color:#991b1b; padding:3px 10px; border-radius:20px; font-size:0.78rem; font-weight:600; }
.badge-medio { background:#fef3c7; color:#92400e; padding:3px 10px; border-radius:20px; font-size:0.78rem; font-weight:600; }
.badge-bajo { background:#d1fae5; color:#065f46; padding:3px 10px; border-radius:20px; font-size:0.78rem; font-weight:600; }

.stat-box {
    background: white;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.stat-num { font-family: 'DM Serif Display', serif; font-size: 2.4rem; color: #1a1d2e; line-height: 1; }
.stat-label { font-size: 0.78rem; color: #6b7280; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.05em; }

.mc-header { font-family: 'DM Serif Display', serif; font-size: 2rem; color: #1a1d2e; margin-bottom: 0.2rem; }
.mc-sub { color: #6b7280; font-size: 0.95rem; margin-bottom: 1.5rem; }

.stProgress > div > div > div > div { background-color: #5b6af0 !important; }

.stTextArea textarea {
    border-radius: 12px !important;
    border: 1.5px solid #e5e7eb !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
}
.stButton > button {
    background: #5b6af0 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
}
.stButton > button:hover {
    background: #4a59e0 !important;
    box-shadow: 0 4px 12px rgba(91,106,240,0.3) !important;
}

.timeline-entry {
    border-left: 3px solid #e5e7eb;
    padding-left: 1.2rem;
    margin-bottom: 1.2rem;
    position: relative;
}
.timeline-entry::before {
    content: '';
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #5b6af0;
    position: absolute;
    left: -6.5px;
    top: 5px;
}
.timeline-date { font-size: 0.78rem; color: #9ca3af; font-weight: 500; text-transform: uppercase; letter-spacing: 0.04em; }
.timeline-text { color: #374151; font-size: 0.92rem; margin: 4px 0; line-height: 1.5; font-style: italic; }
.timeline-result { font-size: 0.85rem; color: #4b5563; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar nav ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1rem 0 1.5rem;'>
        <div style='font-family: DM Serif Display, serif; font-size: 1.6rem; color: #e0e6f0;'>🧠 MindCheck</div>
        <div style='font-size: 0.78rem; color: #6b7280; margin-top: 4px;'>Salud Mental · IA Predictiva</div>
    </div>
    """, unsafe_allow_html=True)

    vista = st.radio("Vista", ["👤  Paciente", "🩺  Psicólogo"], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("<div style='font-size:0.78rem; color:#4b5563;'>Demo NTT Data Hackathon 2026</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  VISTA PACIENTE
# ══════════════════════════════════════════════════════════════════════════════
if vista == "👤  Paciente":

    col_main, col_hist = st.columns([1.1, 0.9], gap="large")

    with col_main:
        st.markdown("<div class='mc-header'>¿Cómo te sientes hoy?</div>", unsafe_allow_html=True)
        st.markdown("<div class='mc-sub'>Cuéntanos en tus propias palabras. Tu análisis es confidencial.</div>", unsafe_allow_html=True)

        texto_usuario = st.text_area(
            label="texto",
            placeholder="Escribe aquí cómo te has sentido hoy, qué pensamientos has tenido, cómo ha ido el día...",
            height=180,
            max_chars=1000,
            label_visibility="collapsed",
        )
        chars = len(texto_usuario)
        st.markdown(f"<div style='font-size:0.8rem; color:#9ca3af; text-align:right; margin-top:-8px;'>{chars} / 1000</div>", unsafe_allow_html=True)

        analizar = st.button("Analizar mi estado →", use_container_width=True)

        if analizar:
            if not texto_usuario.strip():
                st.warning("Escribe algo antes de analizar.")
            else:
                with st.spinner("Analizando..."):
                    resultado_obtenido = None
                    try:
                        response = requests.post(f"{API_URL}/predict", json={"texto": texto_usuario}, timeout=30)
                        if response.status_code == 200:
                            r = response.json()
                            resultado_obtenido = {
                                "prob": r.get("probabilidad", 0),
                                "nivel": r.get("nivel_riesgo", ""),
                                "pred": r.get("prediccion", ""),
                                "demo": False
                            }
                    except requests.exceptions.RequestException:
                        prob_demo = round(random.uniform(20, 85), 1)
                        nivel_demo = "Alto" if prob_demo >= 60 else ("Medio" if prob_demo >= 30 else "Bajo")
                        pred_demo = "Busca ayuda profesional" if nivel_demo == "Alto" else ("Presta atención a tu bienestar mental" if nivel_demo == "Medio" else "Estás bien, sigue cuidando tu salud mental")
                        resultado_obtenido = {
                            "prob": prob_demo,
                            "nivel": nivel_demo,
                            "pred": pred_demo,
                            "demo": True
                        }

                    if resultado_obtenido:
                        prob = resultado_obtenido["prob"]
                        nivel = resultado_obtenido["nivel"]
                        pred = resultado_obtenido["pred"]

                        if nivel == "Alto":
                            badge = "badge-alto"; emoji = "🔴"
                        elif nivel == "Medio":
                            badge = "badge-medio"; emoji = "🟡"
                        else:
                            badge = "badge-bajo"; emoji = "🟢"

                        if resultado_obtenido["demo"]:
                            st.info("🔌 API no disponible — resultado de demo simulado")

                        st.markdown(f"""
                        <div class='mc-card mc-card-accent' style='margin-top:1.2rem;'>
                            <div style='display:flex; align-items:center; gap:10px; margin-bottom:0.8rem;'>
                                <span style='font-size:1.4rem;'>{emoji}</span>
                                <span class='{badge}'>{nivel}</span>
                            </div>
                            <div style='font-family: DM Serif Display, serif; font-size:1.8rem; color:#1a1d2e; line-height:1.2;'>{prob:.1f}% de riesgo</div>
                            <div style='color:#6b7280; font-size:0.9rem; margin-top:6px;'>{pred}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.progress(int(min(prob, 100)))

                        if nivel == "Alto":
                            st.error("💙 Recuerda que no estás solo/a. Considera hablar con un profesional.")
                        elif nivel == "Medio":
                            st.warning("🌿 Cuídate. Pequeños hábitos saludables marcan la diferencia.")
                        else:
                            st.success("✨ ¡Buen estado! Sigue con tus rutinas de bienestar.")

    with col_hist:
        st.markdown("<div style='font-size:1.1rem; font-weight:600; color:#1a1d2e; margin-bottom:0.3rem;'>📋 Mis registros</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.82rem; color:#9ca3af; margin-bottom:1rem;'>Últimos 7 días · Carlos M.</div>", unsafe_allow_html=True)

        registros = PACIENTES_DEMO["Carlos M."]
        probs = [r["probabilidad"] for r in registros]
        avg = sum(probs) / len(probs)
        max_p = max(probs)
        dias_alto = sum(1 for r in registros if r["nivel"] == "Alto")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""<div class='stat-box'>
                <div class='stat-num'>{avg:.0f}%</div>
                <div class='stat-label'>Media riesgo</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='stat-box'>
                <div class='stat-num'>{max_p:.0f}%</div>
                <div class='stat-label'>Pico máximo</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='stat-box'>
                <div class='stat-num'>{dias_alto}</div>
                <div class='stat-label'>Días alto</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        for reg in reversed(registros):
            fecha_str = reg["fecha"].strftime("%A %d %b").capitalize()
            badge_class = "badge-alto" if reg["nivel"] == "Alto" else ("badge-medio" if reg["nivel"] == "Medio" else "badge-bajo")
            st.markdown(f"""
            <div class='timeline-entry'>
                <div class='timeline-date'>{fecha_str} · <span class='{badge_class}'>{reg['nivel']}</span> · {reg['probabilidad']:.0f}%</div>
                <div class='timeline-text'>"{reg['texto'][:120]}{'...' if len(reg['texto']) > 120 else ''}"</div>
                <div class='timeline-result'>{reg['prediccion']}</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  VISTA PSICÓLOGO
# ══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown("<div class='mc-header'>Panel del Psicólogo</div>", unsafe_allow_html=True)
    st.markdown("<div class='mc-sub'>Seguimiento de pacientes · Evolución del riesgo</div>", unsafe_allow_html=True)

    col_sel, _ = st.columns([0.3, 0.7])
    with col_sel:
        paciente_sel = st.selectbox("Paciente", list(PACIENTES_DEMO.keys()), label_visibility="collapsed")

    registros = PACIENTES_DEMO[paciente_sel]
    probs = [r["probabilidad"] for r in registros]
    fechas = [r["fecha"].strftime("%d/%m") for r in registros]
    niveles = [r["nivel"] for r in registros]
    avg = sum(probs) / len(probs)
    tendencia = probs[-1] - probs[-2]
    dias_alto = sum(1 for n in niveles if n == "Alto")
    dias_bajo = sum(1 for n in niveles if n == "Bajo")

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""<div class='stat-box'>
            <div class='stat-num'>{avg:.1f}%</div>
            <div class='stat-label'>Riesgo medio 7d</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        arrow = "↑" if tendencia > 0 else "↓"
        color = "#ef4444" if tendencia > 0 else "#10b981"
        st.markdown(f"""<div class='stat-box'>
            <div class='stat-num' style='color:{color};'>{arrow} {abs(tendencia):.1f}%</div>
            <div class='stat-label'>Tendencia hoy</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class='stat-box'>
            <div class='stat-num' style='color:#ef4444;'>{dias_alto}</div>
            <div class='stat-label'>Días en riesgo alto</div>
        </div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class='stat-box'>
            <div class='stat-num' style='color:#10b981;'>{dias_bajo}</div>
            <div class='stat-label'>Días en riesgo bajo</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    col_chart, col_detail = st.columns([1.4, 0.6], gap="large")

    with col_chart:
        import pandas as pd
        import altair as alt

        source = pd.DataFrame({"Fecha": fechas, "Riesgo": probs, "Nivel": niveles})

        line = alt.Chart(source).mark_line(
            color="#5b6af0", strokeWidth=2.5, interpolate="monotone"
        ).encode(
            x=alt.X("Fecha:O", axis=alt.Axis(labelAngle=0, labelFontSize=12, title=None)),
            y=alt.Y("Riesgo:Q", scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(title="Riesgo (%)", labelFontSize=12)),
        )

        points = alt.Chart(source).mark_point(filled=True, size=100).encode(
            x="Fecha:O",
            y="Riesgo:Q",
            color=alt.Color("Nivel:N", scale=alt.Scale(
                domain=["Alto", "Medio", "Bajo"],
                range=["#ef4444", "#f59e0b", "#10b981"]
            ), legend=alt.Legend(title="Nivel")),
            tooltip=["Fecha", "Riesgo", "Nivel"]
        )

        ref_alto = alt.Chart(pd.DataFrame({"y": [60]})).mark_rule(
            color="#ef4444", strokeDash=[4, 4], opacity=0.4
        ).encode(y="y:Q")

        ref_medio = alt.Chart(pd.DataFrame({"y": [30]})).mark_rule(
            color="#f59e0b", strokeDash=[4, 4], opacity=0.4
        ).encode(y="y:Q")

        chart = (ref_alto + ref_medio + line + points).properties(height=280).configure_view(
            strokeWidth=0
        ).configure_axis(grid=True, gridColor="#f3f4f6")

        st.markdown("<div class='mc-card'><div style='font-weight:600; color:#1a1d2e; margin-bottom:0.8rem;'>📈 Evolución del riesgo — Últimos 7 días</div>", unsafe_allow_html=True)
        st.altair_chart(chart, use_container_width=True)
        st.markdown("""
        <div style='display:flex; gap:1.5rem; font-size:0.78rem; color:#6b7280; margin-top:-8px;'>
            <span>🔴 Alto (&gt;60%)</span><span>🟡 Medio (30–60%)</span><span>🟢 Bajo (&lt;30%)</span>
        </div></div>""", unsafe_allow_html=True)

    with col_detail:
        st.markdown("<div class='mc-card'><div style='font-weight:600; color:#1a1d2e; margin-bottom:1rem;'>🗒️ Entradas del paciente</div>", unsafe_allow_html=True)

        for reg in reversed(registros):
            badge_class = "badge-alto" if reg["nivel"] == "Alto" else ("badge-medio" if reg["nivel"] == "Medio" else "badge-bajo")
            fecha_str = reg["fecha"].strftime("%d/%m")
            st.markdown(f"""
            <div style='border-bottom:1px solid #f3f4f6; padding-bottom:0.8rem; margin-bottom:0.8rem;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <span style='font-size:0.78rem; color:#9ca3af;'>{fecha_str}</span>
                    <span class='{badge_class}'>{reg['probabilidad']:.0f}%</span>
                </div>
                <div style='font-size:0.83rem; color:#4b5563; margin-top:4px; font-style:italic; line-height:1.45;'>"{reg['texto'][:90]}{'...' if len(reg['texto']) > 90 else ''}"</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Alerta clínica automática
    altos_seguidos = 0
    for r in reversed(registros):
        if r["nivel"] == "Alto":
            altos_seguidos += 1
        else:
            break

    if altos_seguidos >= 2:
        st.error(f"⚠️ **Alerta clínica:** {paciente_sel} lleva {altos_seguidos} días consecutivos en nivel ALTO. Se recomienda contacto urgente.")
    elif avg > 55:
        st.warning(f"🟡 **Atención:** El riesgo medio de {paciente_sel} supera el 55% esta semana. Considere aumentar la frecuencia de sesiones.")
    else:
        st.success(f"✅ {paciente_sel} muestra una evolución estable. Continúe el seguimiento habitual.")