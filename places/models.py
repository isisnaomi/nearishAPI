from mongoengine import Document, EmbeddedDocument, fields
from django.db import models

class Category(Document):
    name = fields.StringField()

class Place(Document):
    id = fields.StringField(primary_key=True)
    name = fields.StringField()
    rating = fields.DynamicField()
    loc = fields.ListField(fields.DynamicField(null=True))
    lat = fields.FloatField()
    lng = fields.FloatField()
    vicinity = fields.StringField()
    opening_hours = fields.DynamicField(null=True)

    types = fields.DynamicField()
    photo_reference = fields.StringField()

class User(Document):
    name = fields.StringField()
    types = fields.DynamicField(null=True)





