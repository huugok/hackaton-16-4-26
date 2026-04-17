# 🤖 Proyecto IA - Hackathon

> Una solución de Inteligencia Artificial aplicada a problemas reales de negocio

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-latest-red?logo=streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green?logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-latest-orange?logo=scikit-learn&logoColor=white)

---

## 📋 Descripción

Este proyecto consiste en el desarrollo de una solución de Inteligencia Artificial aplicada a un problema real de negocio: **[aqui el problema a solucionar]**.

La aplicación permite a los usuarios **[aqui lo que permite]**, utilizando un modelo de IA que **[explicar que hace el modelo]**.

---

## 🏗️ Arquitectura del sistema

La solución sigue una arquitectura desacoplada en **tres capas**:

| Capa | Tecnología | Descripción |
|------|-----------|-------------|
| **Frontend** | Streamlit | Interfaz interactiva para el usuario |
| **Backend (API)** | FastAPI | Servicio REST para procesar solicitudes |
| **Modelo de IA** | Python + ML | Predicciones con pandas/scikit-learn |

---

## ⚙️ Flujo de funcionamiento

```
┌─────────────────────────────────────────────────────────────┐
│  1️⃣  Usuario introduce datos en la interfaz (Streamlit)      │
│          ⬇                                                   │
│  2️⃣  La aplicación envía la petición a la API               │
│          ⬇                                                   │
│  3️⃣  La API procesa y llama al modelo de IA                 │
│          ⬇                                                   │
│  4️⃣  El modelo genera una predicción                        │
│          ⬇                                                   │
│  5️⃣  La API devuelve el resultado al frontend               │
│          ⬇                                                   │
│  6️⃣  El resultado se muestra al usuario ✅                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura del proyecto

```
hackaton-16-4-26/
│
├── 🎨 app/                      # Interfaz Streamlit
│   ├── main.py
│   └── pages/                   # Páginas adicionales
│
├── 🧠 model/                    # Lógica del modelo IA
│   ├── train.py                 # Entrenamiento del modelo
│   ├── predict.py               # Modelo usado por la API
│   ├── preprocess.py            # Limpieza de datos
│   └── model.pkl                # Modelo de IA entrenado
│
├── 🔌 api/                      # API con FastAPI
│   └── main.py
│
├── 📊 data/                     # Datos
│   ├── raw/                     # Datos brutos
│   └── processed/               # Datos procesados
│
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Este archivo
```

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Descripción |
|-----------|-------------|
| **Python** | Lenguaje de programación principal |
| **Streamlit** | Framework para crear interfaces web |
| **FastAPI** | Framework para APIs REST modernas |
| **scikit-learn** | Biblioteca de Machine Learning |
| **pandas** | Análisis y manipulación de datos |

---

## 🚀 Workflow de desarrollo

El desarrollo del proyecto sigue las siguientes fases:

### 1️⃣ Preparación de datos
- 📥 Recopilación de datos
- 🧹 Limpieza y preprocesamiento
- ✅ Generación de dataset final

### 2️⃣ Desarrollo del modelo
- 🔍 Selección de variables relevantes
- 🏋️ Entrenamiento del modelo
- 📈 Evaluación de resultados
- 💾 Exportación del modelo (model.pkl)

### 3️⃣ Desarrollo de la API
- 🔗 Creación de endpoint `/predict`
- 🧩 Integración del modelo en la API
- 🧪 Testeo de peticiones

### 4️⃣ Desarrollo del frontend
- 🎨 Creación de interfaz con Streamlit
- 📝 Captura de inputs del usuario
- 📊 Visualización de resultados

### 5️⃣ Integración
- 🔀 Conexión entre frontend y API
- 🔄 Pruebas end-to-end

---

## ⚡ Ejecución del proyecto

### 1️⃣ Clonar repositorio
```bash
git clone https://github.com/huugok/hackaton-16-4-26.git
cd hackaton-16-4-26
```

### 2️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3️⃣ Ejecutar API
```bash
uvicorn api.main:app --reload
```

La API estará disponible en: `http://localhost:8000`

### 4️⃣ Ejecutar aplicación
```bash
streamlit run app/main.py
```

La aplicación web se abrirá en: `http://localhost:8501`

---

## ✨ Futuras posibles mejoras

Despliegue en la nube
Mejora del modelo
Añadir autenticación
Integración con bases de datos

Equipo
[Hugo Catalán Pastor] – *
[Rostislav Rusev Levedovych] – *
[Daniel Zanon Barney] – *
[Eva Borrajo de Orozco Gandia] – *

*/Tareas a definir
-Frontend
-Modelo IA
-Backend/API
-Integración / Datos