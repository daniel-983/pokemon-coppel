# Usar la imagen oficial de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos
COPY requirements.txt /app/

# Instalar paquetes y dependencias especificados en requirements.txt
# RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Abrir el puerto 5000
EXPOSE 5000

# Variables de entorno se jalan del .env
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
# ENV FLASK_ENV=production
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED 1

# Definir el comando para correr la aplicación
CMD ["flask", "run"]