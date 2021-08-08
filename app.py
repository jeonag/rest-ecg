from flask import Flask
from flask_restful import Api
from src.resources.routes import initialize_routes

app = Flask(__name__)

# Instance de Api
api = Api(app)

# Inicializamos las rutas de la API
initialize_routes(api)


# run flask
if __name__ == "__main__":
    app.run(debug=True)
