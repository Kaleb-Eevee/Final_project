import discord
from discord.ext import commands
from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow import keras
import numpy as np
import threading
import requests
import os

# Configurar el bot de Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Crear una app Flask
app = Flask(__name__)

# Cargar modelo de TensorFlow/Keras (manejo de errores incluido)
def load_model():
    global model
    try:
        if os.path.exists("modelo_clima_v2.h5"):
            model = keras.models.load_model("modelo_clima_v2.h5")
        else:
            print("Error: El archivo modelo_clima_v2.h5 no existe.")
            model = None
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
        model = None

def predecir_temperatura(datos):
    if model is None:
        return "Modelo no disponible"
    datos = np.array(datos).reshape(1, -1)
    return model.predict(datos)[0][0]

@app.route('/')
def home():
    return "Bienvenido a la API de predicción climática."

@app.route('/predecir', methods=['POST'])
def predecir():
    datos = request.json.get("datos", [])
    if not datos:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    prediccion = predecir_temperatura(datos)
    return jsonify({"prediccion": prediccion})

# Obtener información climática en tiempo real
def get_weather(city):
    API_KEY = "TU_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

@bot.command()
async def clima(ctx, ciudad: str = "Madrid"):
    data = get_weather(ciudad)
    if data:
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        await ctx.send(f"El clima en {ciudad} es {desc} con una temperatura de {temp}°C.")
    else:
        await ctx.send("No se pudo obtener la información del clima.")

@bot.command()
async def prediccion(ctx, *args):
    try:
        datos = list(map(float, args))
        prediccion = predecir_temperatura(datos)
        if isinstance(prediccion, str):
            await ctx.send("Error: El modelo no está disponible.")
        else:
            await ctx.send(f"Predicción de temperatura basada en datos proporcionados: {prediccion:.2f}°C")
    except Exception:
        await ctx.send("Error en la predicción. Ingresa datos numéricos válidos.")

@bot.command()
async def consejos(ctx):
    consejos = [
        "Usa transporte sostenible.",
        "Ahorra energía en casa.",
        "Consume productos locales.",
        "Planta árboles y cuida el medio ambiente.",
        "Reduce el uso de plástico."
    ]
    await ctx.send(f"🌍 Consejos climáticos: {np.random.choice(consejos)}")

# Ejecutar Flask en un hilo
def run_flask():
    app.run(host='0.0.0.0', port=5001)

if __name__ == "__main__":
    load_model()
    threading.Thread(target=run_flask).start()
    bot.run('TU TOKEN VA AQUÍ')




