import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix

#Cargamos datos
df = pd.read_csv("data/procesed/mental_health.csv")

X = df["text"]
y = df["label"]

#Separamos datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

#Convertimos palabras en números, esos números son la importancia de esa palabra en el texto
#Nos quedaremos solo con las 5000 palabras más importantes
#Usamos tanto palabras como bigramas
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))

#Con fit aprende el vocabulario del dataset
#Con transform convierte el texto a números
X_train_vec = vectorizer.fit_transform(X_train)

#Aplicamos la tranformación del texto al test
X_test_vec = vectorizer.transform(X_test)

#Entrenamos el modelo
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)

#Evaluamos el modelo
print("Accuracy:", model.score(X_test_vec, y_test))
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

joblib.dump(model, "model/model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")