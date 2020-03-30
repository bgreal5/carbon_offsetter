from django.db import models


class FlightInfo(models.Model):
    input_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

