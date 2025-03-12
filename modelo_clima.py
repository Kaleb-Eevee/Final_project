import tensorflow as tf
from tensorflow import keras
import numpy as np

# Generar datos ficticios para entrenamiento
np.random.seed(42)
x_train = np.random.rand(200, 3) * 20  # 200 muestras, 3 características

def generate_temperature_data(x):
    return 10 + 0.7 * x[:, 0] + 0.4 * x[:, 1] - 0.3 * x[:, 2] + np.random.randn(len(x)) * 0.5

y_train = generate_temperature_data(x_train)

# Definir un modelo mejorado
model = keras.Sequential([
    keras.layers.Dense(16, activation='relu', input_shape=(3,)),
    keras.layers.Dense(8, activation='relu'),
    keras.layers.Dense(4, activation='relu'),
    keras.layers.Dense(1)  # Salida con predicción de temperatura
])

# Compilar el modelo
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Entrenar el modelo
model.fit(x_train, y_train, epochs=150, verbose=1, batch_size=16)

# Guardar el modelo mejorado
model.save("modelo_clima_v2.h5")

print("Modelo guardado como 'modelo_clima_v2.h5'")