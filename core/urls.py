from django.urls import path
from . import views

urlpatterns = [
    # Landing Page
    path("", views.vocab, name="vocab"),
    
    # Domain URLs
    path("domains/", views.domain_list, name="domain_list"),
    path("domains/new/", views.domain_create, name="domain_create"),
    path("domains/<int:domain_id>/", views.domain_detail, name="domain_detail"),
    path("domains/<int:domain_id>/edit/", views.domain_update, name="domain_update"),

    # Item URLs
    path("domains/<int:domain_id>/items/new/", views.item_create, name="item_create"),
    path("items/<int:item_id>/", views.item_detail, name="item_detail"),
    path("items/<int:item_id>/edit/", views.item_update, name="item_update"),
    path("items/<int:item_id>/delete/", views.item_delete, name="item_delete"),

    # Translation URLs
    path("items/<int:item_id>/translations/new/", views.translation_create, name="translation_create"),
]