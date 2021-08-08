import mongoengine as db

# Inicializamos la Base de Datos
DB_URI = "mongodb+srv://admin:admin@proyecto-titulacion.7wj2y.mongodb.net/DB_back_ecg?retryWrites=true&w=majority"

db.connect(host=DB_URI)
