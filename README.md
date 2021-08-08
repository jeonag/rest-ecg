# Procesamiento de Señales - Infarto Miocardio (MI)
 
Este proyecto permite detectar la anomalía en el segmento ST de la señal ECG que presenta el infarto al miocardio.


# Metodología

  - Obtención de los datos del MIT
  - Implementacion de un algoritmo para detectar el complejo PQRST.
  - Detectar cada uno de los picos del complejo PQRST.
  - Separación del Intervalo S-T en ambas señales.
  - Sacar promediados de los segmentos S-T
  - Encontrar la deformación del segmento S-T
   

### Tecnologías usadas:

* [Python] - <https://www.python.org>
* [Flask] - <https://flask.palletsprojects.com/en/1.1.x/>
* [MongoDB] - <https://www.mongodb.com/es>
* [MongoDB Atlas] - <https://www.mongodb.com/cloud/atlas>
* [FireBase Storage] - <https://firebase.google.com/docs/storage?hl=es-419>
* [Heroku] - <https://www.heroku.com>

### Bibliotecas
 

| Biblioteca | Documentación |
| ------ | ------ |
| mongoengine | <http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/> |
| flask-restful | <https://flask-restful.readthedocs.io/en/latest/> |
| neurokit2 | https://neurokit2.readthedocs.io/en/latest/functions.html#module-neurokit2.ecg |
| mongoengine-goodjson | https://pypi.org/project/mongoengine-goodjson/ |
| pandas | https://pandas.pydata.org/docs/getting_started/index.html#getting-started | 


### Routes
 

|  |  |
| ------ | ------ |
| señal | <https://back-ecg.herokuapp.com/api/signals>|
| imagenes | <https://back-ecg.herokuapp.com/api/images/signal> |

## Documentación
<https://www.dropbox.com/s/l2vunrb2a2hpbce/Informe.pdf?dl=0>


## Developers

* Back-End : Jhon Oña
* Front-End : Carlos Campoverde (https://github.com/miocardio-ecg/front-end.git)
 
Universidad Central del Ecuador
 
