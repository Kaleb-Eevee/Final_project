import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
from config import MODEL_PATH

# Cargar el modelo de IA
def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = keras.models.load_model(MODEL_PATH)
    else:
        print("Error: El modelo no existe.")
        model = None

# Hacer una predicción
def predict_temperature(data):
    if model is None:
        return "Modelo no disponible"
    data = np.array(data).reshape(1, -1)
    return model.predict(data)[0][0]

# Cargar modelo al iniciar
load_model()
