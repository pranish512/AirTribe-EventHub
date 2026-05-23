from rest_framework.routers import DefaultRouter

# project
from .views import ReservationViewSet, EventViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'reservations', ReservationViewSet, basename='reservation')
urlpatterns = router.urls