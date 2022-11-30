#from datetime import datetime
from django.db import models
from django.utils import timezone
from Aerospike.aerospike import AerospikeCacheControl

def expensive_calculation():
    return timezone.now()

class Poll(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=expensive_calculation)
    
    def save(self):
        keys_to_clear = [self.pk, "home"]
        acc = AerospikeCacheControl()
        keys_to_clear = acc.generate_multiples_keys(keys_to_clear)
        print(acc.delete_array_value_on_cache(keys_to_clear))
        return super().save()
