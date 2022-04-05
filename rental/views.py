from .models import Rental, Reservation
from django.views.generic.list import ListView
from django.db.models import OuterRef, Subquery


class ReservationsListView(ListView):
    template_name = "rental/index.html"
    model = Reservation
    context_object_name = "reservation_list"

    def get_queryset(self, *args, **kwargs):
        newest = Reservation.objects.filter(
            rental_id=OuterRef("rental_id"), checkout__lt=OuterRef("checkin")
        )
        rental = Rental.objects.filter(id=OuterRef("rental_id"))
        qs = Reservation.objects.annotate(
            previous=Subquery(
                newest.values("id").order_by("-checkin")[:1],
            ),
            rental_name=Subquery(rental.values("name")[:1])
        ).order_by("checkin")
        return qs
