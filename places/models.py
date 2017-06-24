from mongoengine import Document, EmbeddedDocument, fields
from django.db import models

class Category(Document):
    name = fields.StringField()

class Place(Document):
    id = fields.StringField(primary_key=True)
    name = fields.StringField()
    rating = fields.DynamicField()
    loc = fields.PointField()
    lat = fields.FloatField()
    lng = fields.FloatField()
    vicinity = fields.StringField()
    opening_hours = fields.DynamicField(null=True)

    types = fields.DynamicField(null=True)
    photo_reference = fields.StringField()
    user_rated = fields.StringField()

class User(Document):
    name = fields.StringField()
    types = fields.ListField(fields.StringField())


class RatedPlace(Document):
    place_id = fields.StringField()
    user_id = fields.StringField()
    rating = fields.DynamicField()


