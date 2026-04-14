from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemberViewSet, TrainerViewSet, GymClassViewSet

router = DefaultRouter()
router.register('members', MemberViewSet)
router.register('trainers', TrainerViewSet)
router.register('classes', GymClassViewSet)

urlpatterns = [
    path('', include(router.urls)),
]