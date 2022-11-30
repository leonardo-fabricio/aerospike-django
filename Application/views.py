from django.http import HttpResponse, JsonResponse
from Aerospike.aerospike import *
from .models import *
from .serializer import *
from rest_framework import generics, serializers

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('__all__')


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

class home(generics.ListAPIView):
    serializer_class = PollSerializer

    def create_cache(self):
        acc = AerospikeCacheControl("home")
        instances = list(Poll.objects.all().values())
        data = {"offers": instances}
        acc.save_in_cache(data)
        print("Nao acessei a cache")
        return instances
    
    def get_queryset(self):
        acc = AerospikeCacheControl("home")
        product = acc.get_value_on_cache()
        return product["offers"] if product != None else self.create_cache()
        
