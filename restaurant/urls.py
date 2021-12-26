from rest_framework import routers

from restaurant.views import RestaurantViewSet

router = routers.SimpleRouter()
router.register(r'restaurant', RestaurantViewSet, basename='restaurant')
urlpatterns = router.urls
