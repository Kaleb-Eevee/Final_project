from flask import Flask, request, jsonify
from model import predict_temperature

app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenido a la API de predicción climática."

@app.route('/predecir', methods=['POST'])
def predecir():
    datos = request.json.get("datos", [])
    if not datos:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    prediccion = predict_temperature(datos)
    return jsonify({"prediccion": prediccion})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
