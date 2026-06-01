from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from ..models import Domain, Item, Translation
from .serializers import DomainSerializer, ItemSerializer, TranslationSerializer

@extend_schema(tags=["Domains"])
class DomainViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    lookup_field = 'id'

@extend_schema(tags=["Items"])
class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Item.objects.prefetch_related('translations').all()
    serializer_class = ItemSerializer
    lookup_field = 'id'

@extend_schema(tags=["Translations"])
class TranslationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    lookup_field = 'id' 