from django.db import models

'''
    Ignore - stores info about ignores.
    Area - represents information about all areas stored in POI Data Provider. For now it will be used just to
        remember what is currently in database.

    NOTE: To work with the database in Django you need to "makemigrations" and then "migrate".
    https://docs.djangoproject.com/en/1.7/topics/migrations/
'''


class Ignore(models.Model):
    uuid = models.CharField(max_length=30)
    ignored = models.CharField(max_length=30)


class Area(models.Model):
    lat_id = models.IntegerField()
    lng_id = models.IntegerField()