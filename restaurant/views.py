from rest_framework import viewsets

from .serializers import RestaurantSerializer
from .models import Restaurant


class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
