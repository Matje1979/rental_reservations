from django.urls import path
from .views import ReservationsListView

urlpatterns = [path("", ReservationsListView.as_view(), name="reservation-list")]
