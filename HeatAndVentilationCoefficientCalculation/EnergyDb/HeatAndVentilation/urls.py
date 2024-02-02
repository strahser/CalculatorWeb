from django.urls import path
from django.views import View
from . import views

urlpatterns = [
    path("", views.BuildingListView.as_view(), name="index"),
    # path("", views.index, name="index"),
]