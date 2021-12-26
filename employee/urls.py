from rest_framework.routers import DefaultRouter

from employee import views

router = DefaultRouter()
router.register(r"employee", views.EmployeeViewSet, basename="employee")
urlpatterns = router.urls
