from django.http import HttpResponse, JsonResponse
from Aerospike.aerospike import *
from .models import *
from .serializer import *


def detail(request, pk):
    #cache = get_cache('aerospike_cache.cache://127.0.0.1:3000')
    acc = AerospikeCacheControl(pk)
    product = acc.get_value_on_cache()
    if product:
        print("Acessei a cache")
        return JsonResponse(product)
    instance = Poll.objects.get(pk=pk)
    serializer = PollSerializer(instance=instance, many = False)
    product = acc.save_in_cache(serializer.data)
    print("Não acessei a cache")
    return JsonResponse(product)

def home(request):
    return JsonResponse({})