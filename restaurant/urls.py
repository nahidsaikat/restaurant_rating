from rest_framework import routers

from restaurant.views import RestaurantViewSet

router = routers.SimpleRouter()
router.register(r'restaurants', RestaurantViewSet, basename='restaurants')
urlpatterns = router.urls
