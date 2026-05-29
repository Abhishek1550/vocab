from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DomainViewSet, ItemViewSet, TranslationViewSet

router = DefaultRouter()
router.register(r'domains', DomainViewSet)
router.register(r'items', ItemViewSet)
router.register(r'translations', TranslationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]