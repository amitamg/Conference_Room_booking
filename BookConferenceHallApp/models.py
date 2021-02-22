from django.db import models

# Create your models here.


class Hall(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    Hall = models.ManyToManyField(Hall)
    date = models.DateField()
    comment = models.TextField()

    def __str__(self):
        for r in self.Hall.all():
            return "Date of booking: {}, conference Hall: {}".format(self.date, r.name)
