# Pokemon API

Este repositorio contiene una aplicacion Flask usando MongoDB, Swagger para documentación OpenAPI, JWT para autenticación, Redis para caché, Git para control de versiones, y Docker for contenedorización.

## Prerequisitos

- Python 3.8 or superior
- Cuenta MongoDB Atlas
- Git
- Docker y Docker Compose

## Configuración de MongoDB Atlas
- Registrarse en MongoDB Atlas y verificar la cuenta
- Iniciar sesión en MongoDB Atlas
- Crear un Cluster

## Instalación

1. **Clonar el repositorio**

    ```
    git clone https://mirepositorio.com/pokemon_coppel.git
    cd my_pokemon_api
    ```

2. **Configurar un entorno virtual de Python (opcional)**

    ```
    python3 -m venv venv
    source venv/bin/activate  # En Windows usar `.\venv\Scripts\activate`
    ```

3. **Instalar dependencias**

    ```
    pip install -r requirements.txt

    pip install Flask
    pip install mongoengine
    pip install Flask-PyMongo
    pip install Flask-JWT-Extended
    pip install redis
    pip install flasgger
    pip install gunicorn
    pip install python-dotenv
    pip install pydantic <-- for validation
    pip install requests
    pip install Flask-WTF

    ```

4. **Configurar variables de entorno**

    Copiar el archivo `.env.example` y renombrarlo como `.env`. y actualizar las variables de entorno correspondientes

    ```
    cp .env.example .env
    ```

5. **Configuración Docker**

    Asegurarse de que Docker y Docker Compose están instalados y corriendo en el equipo. Luego compilar y ejecutar los contenedores:

    ```
    docker-compose up --build
    ```

## Ejecutar la aplicación

Después de la instalación, se puede correr la aplicación 
activando el entorno virtual:
    ```
    .\venv\Scripts\Activate
    flask run
    ```

También se puede correr utilizando Docker
Docker:
docker-compose up

## Pruebas
python -m unittest discover -s tests

## Documentacion Swagger API
Una vez que la aplicación está ejecutándose, se puede acceder al UI de Swagger para probar los endpoints en: localhost:11000/apidocs


