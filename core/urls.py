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
]