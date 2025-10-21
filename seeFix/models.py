from django.db import models

# Create your models here.
from mongoengine import Document, StringField, EmailField, DateTimeField
import datetime

class User(Document):
    name = StringField(required=True, max_length=50)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(default="student")
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {"collection": "users"}
