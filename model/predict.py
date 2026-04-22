import joblib
from deep_translator import GoogleTranslator

# cargar modelo entrenado
model = joblib.load("model/model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

def translate_to_english(text_es):
    return GoogleTranslator(source="es", target="en").translate(text_es)

def predict_risk(text):
    if isinstance(text, list):
        text = text[0]
        
    text_en = translate_to_english(text)
    vec = vectorizer.transform([text_en])
    prob = model.predict_proba(vec)[0][1] * 100

    if prob < 30:
        level = "Bajo"
    elif prob < 60:
        level = "Medio"
    else:
        level = "Alto"

    return prob, level


if __name__ == "__main__":
    texto = "Me siento muy triste y sin ganas de nada"
    risk, level = predict_risk(texto)
    print(f"Riesgo: {risk:.2f}% ({level})")