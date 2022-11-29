from django.http import HttpResponse, JsonResponse
from Aerospike.aerospike import *
from .models import *
from .serializer import *


def home(request, pk):
    #cache = get_cache('aerospike_cache.cache://127.0.0.1:3000')
    
    product = get_value_on_cache(pk)
    if product:
        print("Acessei a cache")
        return JsonResponse(product)
    instance = Poll.objects.get(pk=pk)
    serializer = PollSerializer(instance=instance, many = False)
    save_in_cache(serializer.data)
    product = get_value_on_cache(serializer.data["id"])
    print("Não acessei a cache")
    return JsonResponse(product)