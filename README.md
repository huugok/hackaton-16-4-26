# 🤖 Proyecto IA - Hackathon

> Una solución de Inteligencia Artificial aplicada a problemas reales de negocio

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-latest-red?logo=streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green?logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-latest-orange?logo=scikit-learn&logoColor=white)

---

## 📋 Descripción

Este proyecto consiste en el desarrollo de una solución de Inteligencia Artificial aplicada a un problema real de negocio: Imposibilidad del seguimiento de pacientes con posibilidad de enfermedades mentales.

La aplicación permite a los usuarios tener un seguimiento en el avanze del anlisis de riegos de tener enfermedades mentales tales como depresión y ansiedad entre otras, utilizando un modelo de IA que dado una entrada en texto natural hace un predicción del riesgo del paciente.

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
│  1️⃣  Usuario introduce datos en la interfaz (Streamlit)     │
│          ⬇                                                  │
│  2️⃣  La aplicación envía la petición a la API               │
│          ⬇                                                  │
│  3️⃣  La API procesa y llama al modelo de IA                 │
│          ⬇                                                  │
│  4️⃣  El modelo genera una predicción                        │
│          ⬇                                                  │
│  5️⃣  La API devuelve el resultado al frontend               │
│          ⬇                                                  │
│  6️⃣  El resultado se muestra al usuario ✅                  │
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
- Recopilación de datos
- Limpieza y preprocesamiento
- Generación de dataset final

### 2️⃣ Desarrollo del modelo
- Selección de variables relevantes
- Entrenamiento del modelo
- Evaluación de resultados
- Exportación del modelo (model.pkl)

### 3️⃣ Desarrollo de la API
- Creación de endpoint `/predict`
- Integración del modelo en la API
- Testeo de peticiones

### 4️⃣ Desarrollo del frontend
- Creación de interfaz con Streamlit
- Captura de inputs del usuario
- Visualización de resultados

### 5️⃣ Integración
- Conexión entre frontend y API
- Pruebas end-to-end

---

## ⚡ Instalación y configuración del entorno

Sigue estos pasos para ejecutar el proyecto en tu entorno local.

### 📋 Requisitos previos

- **Python 3.10+** ([Descargar Python](https://www.python.org/downloads/))
- **Git** ([Descargar Git](https://git-scm.com/))
- **pip** (incluido con Python)

---

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/huugok/hackaton-16-4-26.git
cd hackaton-16-4-26
```

---

### 2️⃣ Crear entorno virtual

Se recomienda usar un entorno virtual para aislar las dependencias del proyecto:

```bash
python3 -m venv venv
```

> 💡 **Tip:** El entorno virtual crea un espacio aislado con sus propios paquetes de Python.

---

### 3️⃣ Activar el entorno virtual

**🐧 Linux / macOS:**
```bash
source venv/bin/activate
```

**🪟 Windows:**
```bash
venv\Scripts\activate
```

> Si la activación fue exitosa, verás `(venv)` al principio de tu línea de comandos.

---

### 4️⃣ Instalar dependencias

Con el entorno virtual activado, instala todas las dependencias necesarias:

```bash
pip install -r requirements.txt
```

**Alternativa (si tienes problemas):**
```bash
python3 -m pip install -r requirements.txt
```

---

### ⚠️ Notas importantes

| ⚠️ Nota | Descripción |
|--------|-------------|
| **Carpeta venv/** | No subas la carpeta `venv/` a tu repositorio (ya está en `.gitignore`) |
| **Entorno activado** | Asegúrate de que el entorno esté activado antes de instalar paquetes |
| **Actualizaciones** | Para actualizar `pip` usa: `pip install --upgrade pip` |

---

### 🧪 Verifica la instalación

Para confirmar que todo está correctamente instalado, ejecuta:

```bash
python --version
pip list
```


---

## ✨ Futuras posibles mejoras

Despliegue en la nube
Mejora del modelo
Añadir autenticación
Integración con bases de datos

## Equipo
[Hugo Catalán Pastor] – Integracion y datos
[Rostislav Rusev Levedovych] – Frontend
[Daniel Zanon Barney] – Frontend
[Eva Borrajo de Orozco Gandia] – Modelo IA
