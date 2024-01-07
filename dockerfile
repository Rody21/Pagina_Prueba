# Usa una imagen de Python
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia todo el contenido de la carpeta Pagina_Prueba al contenedor
COPY . /app

# Instala las dependencias del proyecto
RUN pip install -r /app/app/requirements.txt

# Comando para ejecutar la aplicación Flask cuando el contenedor se inicie
CMD ["python", "/app/app/app.py"]
