from django.urls import path
from .views import ReservationsList

urlpatterns = [path("", ReservationsList.as_view(), name="reservation-list")]
