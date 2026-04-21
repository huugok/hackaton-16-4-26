import joblib
import os
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

print("Iniciando el entrenamiento del modelo...")

# 1. Datos de prueba básicos
textos = ["me siento genial", "estoy muy feliz", "tengo mucha ansiedad", "no puedo dormir me ahogo"]
etiquetas = [0, 0, 1, 1]

# 2. Crear y entrenar el modelo
modelo = make_pipeline(TfidfVectorizer(), LogisticRegression())
modelo.fit(textos, etiquetas)

# 3. Calcular la ruta EXACTA donde guardar el archivo
# Esto busca la carpeta donde está este script (model/) y guarda model.pkl ahí mismo
ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_guardado = os.path.join(ruta_actual, "model.pkl")

# 4. Guardar el modelo
joblib.dump(modelo, ruta_guardado)

print(f"¡ÉXITO! Modelo guardado correctamente en:\n{ruta_guardado}")
# Comprobación de peso
peso = os.path.getsize(ruta_guardado)
print(f"El archivo pesa: {peso} bytes (Si es mayor a 0, ¡está perfecto!)")