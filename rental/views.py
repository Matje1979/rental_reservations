from re import template
from django.shortcuts import render
from .models import Rental, Reservation
from django.views.generic.list import ListView


class ReservationsList(ListView):
    template_name = "rental/index.html"
    model = Reservation
    context_object_name = "reservation_list"
    
    def get_queryset(self, *args, **kwargs):
        # qs = Reservation.objects.all().annotate(
        #     previous = Subquery(
                
        #     )
        # )
        # return qs
        pass