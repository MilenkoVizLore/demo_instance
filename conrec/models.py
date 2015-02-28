from django.db import models


class Ignore(models.Model):
    uuid = models.CharField(max_length=30)
    ignored = models.CharField(max_length=30)
