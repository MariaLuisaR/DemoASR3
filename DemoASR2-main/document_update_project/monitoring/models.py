from django.db import models

class Server(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    uptime = models.DurationField()
    response_time = models.DurationField()

    def __str__(self):
        return self.name
