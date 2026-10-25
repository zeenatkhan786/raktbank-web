from django.urls import path

from . import views

app_name = "bank"

urlpatterns = [
    path("", views.home, name="home"),

    path("donors/", views.donor_list, name="donor_list"),
    path("donors/add/", views.donor_add, name="donor_add"),
    path("donors/<int:pk>/edit/", views.donor_edit, name="donor_edit"),
    path("donors/<int:pk>/delete/", views.donor_delete, name="donor_delete"),

    path("availability/", views.availability, name="availability"),
    path("availability/<int:pk>/update/", views.stock_edit, name="stock_edit"),

    path("requests/", views.request_list, name="request_list"),
    path("requests/new/", views.request_add, name="request_add"),
    path("requests/<int:pk>/edit/", views.request_edit, name="request_edit"),
    path("requests/<int:pk>/status/", views.request_status, name="request_status"),
    path("requests/<int:pk>/delete/", views.request_delete, name="request_delete"),
]
