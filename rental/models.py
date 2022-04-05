from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from .validators import validate_date


class Rental(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    rental_id = models.ForeignKey(Rental, on_delete=models.CASCADE)
    checkin = models.DateField(validators=[validate_date])
    checkout = models.DateField(validators=[validate_date])

    def __str__(self):
        return f"""Reservation rental num: {self.rental_id}
        ({self.checkin.isoformat()}/{self.checkout.isoformat()})"""

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        # Checking if the combination of checkin and checkout dates is valid.
        if self.checkin >= self.checkout:
            raise ValidationError(
                message="Checkin date must be earlier than checkout date!",
            )

    def validate_unique(self, *args, **kwargs):
        super().validate_unique(*args, **kwargs)
        # Checking if there is an overlapping reservation.
        if self.__class__.objects.filter(
            Q(
                rental_id=self.rental_id,
                checkin__lt=self.checkin,
                checkout__gt=self.checkin,
            )
            | Q(
                rental_id=self.rental_id,
                checkin__lt=self.checkout,
                checkout__gt=self.checkout,
            )
            | Q(
                rental_id=self.rental_id,
                checkin__gt=self.checkin,
                checkout__lt=self.checkout,
            )
        ).exists():
            raise ValidationError(
                message="Reservation for this rental within this period already exists",
                code="unique_together",
            )
