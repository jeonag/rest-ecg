from src.resources.signal_controller import SignalGetPostApi, SignalPutDelGetIdApi
from src.resources.image_controller import AnalisisSignal

def initialize_routes(api):
    # rutas señal
    api.add_resource(SignalGetPostApi, '/api/signals')
    api.add_resource(SignalPutDelGetIdApi, '/api/signals/<name>')
    # rutas imagenes
    api.add_resource(AnalisisSignal, '/api/images/<name>')


