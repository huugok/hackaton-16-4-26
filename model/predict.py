import joblib

# cargar modelo entrenado
model = joblib.load("model/model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")


def predict_risk(text):
    vec = vectorizer.transform([text])
    prob = model.predict_proba(vec)[0][1] * 100

    if prob < 30:
        level = "Bajo"
    elif prob < 70:
        level = "Medio"
    else:
        level = "Alto"

    return prob, level


if __name__ == "__main__":
    texto = "I feel very sad and hopeless lately"
    risk, level = predict_risk(texto)
    print(f"Riesgo: {risk:.2f}% ({level})")