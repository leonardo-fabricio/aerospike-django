#from datetime import datetime
from django.db import models
from django.utils import timezone
from Aerospike.aerospike import delete_value_on_cache

def expensive_calculation():
    return timezone.now()

class Poll(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=expensive_calculation)
    
    def save(self):
        delete_value_on_cache(self.pk)
        return super().save()
