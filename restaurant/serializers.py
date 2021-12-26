from django.utils import timezone
from rest_framework import serializers

from restaurant import models
from restaurant.exceptions import MenuExistsException


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Restaurant
        fields = '__all__'


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FoodItem
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Menu
        fields = '__all__'

    def validate(self, attrs):
        is_exists = models.Menu.objects.filter(
            date=timezone.now().date(),
            restaurant=attrs.get("restaurant")).exists()
        if is_exists:
            raise MenuExistsException("Menu already exists for today.")
        return attrs

    def create(self, validated_data):
        validated_data["date"] = timezone.now().date()
        return super().create(validated_data)


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vote
        fields = '__all__'

    def validate(self, attrs):
        attrs["employee"] = self.context["request"].user
        is_exists = models.Vote.objects.filter(
            date=timezone.now().date(),
            restaurant=attrs.get("restaurant"),
            employee=self.context["request"].user,
        ).exists()
        if is_exists:
            raise MenuExistsException("Already voted for the restaurant.")
        return attrs
