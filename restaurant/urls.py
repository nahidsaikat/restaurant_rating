from rest_framework import routers

from restaurant import views

router = routers.SimpleRouter()
router.register(r'restaurant', views.RestaurantViewSet, basename='restaurant')
router.register(r'food_item', views.FoodItemViewSet, basename='food_item')
router.register(r'menu', views.MenuViewSet, basename='menu')
router.register(r'vote', views.VoteViewSet, basename='vote')
urlpatterns = router.urls
