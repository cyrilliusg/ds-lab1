from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    work = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.name}"
