from src.mongoDB.db import db
import mongoengine_goodjson as gj


# Esta clase crea el Schema Signal en mongoDB
class Signal(gj.Document):
    name = db.StringField(required=True)
    signal = db.ListField()
