from flask import Response, request
from flask_restful import Resource
from src.mongoDB.models.signal import Signal


class SignalGetPostApi(Resource):
    # Este metodo obtiene las señales guardadas en la base de datos
    def get(self):
        companies = Signal.objects().to_json()
        return Response(companies, mimetype="application/json", status=200)

    # Este metodo permite ingresar una nueva señal
    def post(self):
        try:
            body = request.get_json(force=True)
            signal = Signal(**body).save()
            id = signal.id
            return {"mensaje": "señal creadas", 'id': str(id)}, 200
        except Exception as e:
            return "Error \n %s" % (e)


class SignalPutDelGetIdApi(Resource):
    # Este metodo permite actualizar una señal
    def put(self, id):
        try:
            body = request.get_json()
            Signal.objects.get(id=id).update(**body)
            return {'mensaje': "campos actualizados"}, 200
        except Exception as e:
            return "Error \n %s" % (e)

    # Este metodo permite eliminar una señal ingresando su id, ejemplo: api/signals/id
    def delete(self, id):
        try:
            Signal.objects.get(id=id).delete()
            return id + ' Eliminado', 200
        except Exception as e:
            return "Error \n %s" % (e)

    # Este metodo permite obtener una señal por su id, ejemplo: api/signals/id
    def get(self, name):
        try:
            signal = Signal.objects.get(name=name).to_json()
            return Response(signal, mimetype="application/json", status=200)
        except Exception as e:
            return "Error \n %s" % (e)


