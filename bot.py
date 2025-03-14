# Archivo: bot.py
import discord
from discord.ext import commands
import requests
import threading
import numpy as np
from config import DISCORD_TOKEN, API_KEY
from flask_server import app
from model import predecir_temperatura

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

@bot.command()
async def clima(ctx, ciudad: str = "Mexico City"):
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
        await ctx.send(f"Predicción de temperatura: {prediccion:.2f}°C")
    except Exception:
        await ctx.send("Error en la predicción. Asegúrate de ingresar datos numéricos válidos.")

@bot.command()
async def consejos(ctx):
    consejos = [
        "Usa menos plásticos de un solo uso.",
        "Reduce el consumo de energía en casa.",
        "Utiliza transporte público o bicicleta en lugar de automóvil.",
        "Planta árboles y ayuda a conservar la naturaleza.",
        "Reduce el desperdicio de agua y alimentos."
    ]
    await ctx.send(f"🌍 Consejos para combatir el cambio climático: {np.random.choice(consejos)}")

def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run(DISCORD_TOKEN)






