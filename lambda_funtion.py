import os
import requests
import json
import pymysql

DB_host = os.environ["DB_HOST"]
DB_user = os.environ["DB_USER"]
DB_password = os.environ["DB_PASSWORD"]
DB_name = os.environ["DB_NAME"]


api_KEY = os.environ["COIN_APY_KEY"]
target = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
headers = {"X-CMC_PRO_API_KEY": api_KEY}
parameters = {"symbol": "BTC,ETH"}


def lambda_handler(event, context):
    # Hacer llamado a la API
    try:
        response = requests.get(target, headers=headers, params=parameters)

        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            try:
                # Respuesta en formato JSON
                data = response.json()

                Name_BTC = data["data"]["BTC"]["name"]
                Price_BTC = data["data"]["BTC"]["quote"]["USD"]["price"]
                Time_BTC = data["data"]["BTC"]["quote"]["USD"]["last_updated"]

                Name_ETH = data["data"]["ETH"]["name"]
                Price_ETH = data["data"]["ETH"]["quote"]["USD"]["price"]
                Time_ETH = data["data"]["ETH"]["quote"]["USD"]["last_updated"]

                print(Name_BTC, Price_BTC, Time_BTC)
                print(Name_ETH, Price_ETH, Time_ETH)

            except requests.exceptions.JSONDecodeError as e:
                print("Error al decodificar JSON:", e)
        else:
            print(
                "La solicitud GET no fue exitosa. Código de estado:",
                response.status_code,
            )
    except requests.exceptions.RequestException as e:
        print("Error de solicitud:", e)

    try:
        connector = pymysql.connect(
            host=DB_host, user=DB_user, password=DB_password, database=DB_name
        )
        cursor = connector.cursor()
        query = (
            "INSERT INTO Monedas (Name, Symbol, Price, Time) VALUES (%s, %s, %s, %s)"
        )
        cursor.execute(query, (Name_BTC, "BTC", Price_BTC, Time_BTC))
        cursor.execute(query, (Name_ETH, "ETH", Price_ETH, Time_ETH))
        connector.commit()
        cursor.close()
        connector.close()
        print("Datos insertados correctamente.")
    except pymysql.Error as e:
        print("Error al insertar datos:", e)
    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}
