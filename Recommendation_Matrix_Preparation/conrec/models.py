from django.db import models

'''
    Ignore stores info about ignores.
    NOTE: To work with the database in Django you need to "makemigrations" and then "migrate".
    https://docs.djangoproject.com/en/1.7/topics/migrations/
'''


class Ignore(models.Model):
    uuid = models.CharField(max_length=60)
    ignored = models.CharField(max_length=60)


class Area(models.Model):
    name = models.CharField(max_length=60)
    lat_id = models.IntegerField()
    lng_id = models.IntegerField()


class Keys(models.Model):
    temp = models.CharField(max_length=60)
    real = models.CharField(max_length=60)
    time = models.DateTimeField(auto_now=True, auto_now_add=False)


class RecommendationMatrix(models.Model):
    name = models.CharField(max_length=60)
    data = models.CharField(max_length=8192)
