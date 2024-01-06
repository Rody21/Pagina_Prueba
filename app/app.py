from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
import pymysql
import os
import json

load_dotenv()

app = Flask(__name__)

# Configuración para la conexión a la base de datos
db_params = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "db": os.getenv("DB_NAME"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}


def obtener_datos():
    try:
        connection = pymysql.connect(**db_params)
        cursor = connection.cursor()
        query = "SELECT * FROM Monedas"
        cursor.execute(query)
        data = cursor.fetchall()  # Obtener todos los datos

        cursor.close()
        connection.close()

        print(data)
        return data
    except Exception as e:
        return {"error": str(e)}


@app.route("/")
def index():
    # Obtener los datos una vez
    datos = obtener_datos()

    return render_template("index.html", datos=json.dumps(datos))


@app.route("/get_data")
def get_data():
    # Reutilizar la función para obtener datos
    datos = obtener_datos()
    return jsonify(datos)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
