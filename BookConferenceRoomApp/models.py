from django.db import models

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    room = models.ManyToManyField(Room)
    date = models.DateField()
    comment = models.TextField()

    def __str__(self):
        for r in self.room.all():
            return "Date of booking: {}, conference room: {}".format(self.date, r.name)
