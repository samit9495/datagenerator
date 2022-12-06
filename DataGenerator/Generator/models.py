from django.db import models


# Create your models here.


class category(models.Model):
    Name = models.CharField(max_length=50)
    length = models.IntegerField()
    sequence = models.CharField(max_length=100)
    case = models.CharField(max_length=20)
    type = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sequence', 'case'], name='Unique Sequence')
        ]