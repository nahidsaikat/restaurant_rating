import datetime

from django.db.models import Count
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from restaurant import serializers
from restaurant import models


class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RestaurantSerializer
    queryset = models.Restaurant.objects.all()
    permission_classes = [IsAuthenticated]


class FoodItemViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FoodItemSerializer
    queryset = models.FoodItem.objects.all()
    permission_classes = [IsAuthenticated]


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MenuSerializer
    queryset = models.Menu.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def get_menu(self, request):
        restaurant_id = request.GET.get('restaurant_id')
        menu = models.Menu.objects.filter(
            restaurant_id=restaurant_id,
            date=timezone.now().date()
        ).get()
        return Response(serializers.MenuSerializer(instance=menu).data)


class VoteViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VoteSerializer
    queryset = models.Vote.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        data["employee"] = request.user.id
        data["date"] = timezone.now().date()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def get_winner(self, request):
        data = {}
        date = timezone.now().date()
        result = models.Result.objects.filter(date=date)
        if not result:
            result_list = models.Vote.objects.filter(date=date)\
                .annotate(total=Count("restaurant")).order_by("-total")
            for item in result_list:
                pre_date = timezone.now().date() - datetime.timedelta(days=3)
                pre_results = models.Result.objects.filter(winner=item.restaurant, date__gte=pre_date)
                if len(pre_results) >= 3:
                    continue
                result = models.Result.objects.create(date=date, winner=item.restaurant)
                data = serializers.RestaurantSerializer(instance=result.winner).data
                break
        return Response(data=data)
