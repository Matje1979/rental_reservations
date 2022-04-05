from django.forms import ValidationError
from django.test import TestCase
from .models import Rental, Reservation
from datetime import date


class ReservationTestCase(TestCase):
    def setUp(self) -> None:
        self.rental = Rental.objects.create(name="Rental 1")

    def test_reservation_OK(self):
        Reservation.objects.create(
            rental_id=self.rental.id,
            checkin=date(1999, 10, 10),
            checkout=date(1999, 10, 12),
        )
        self.assertEqual(Reservation.objects.count(), 1)

    def test_reservation_date_combination_invalid(self):
        with self.assertRaises(ValidationError) as exc:
            Reservation.objects.create(
                rental_id=self.rental.id,
                checkin=date(1999, 10, 14),
                checkout=date(1999, 10, 12),
            )
        self.assertIn(
            "Checkin date must be earlier than checkout date!",
            exc.exception.messages,
        )
        self.assertEqual(Reservation.objects.count(), 0)

    def test_reservation_date_format_invalid(self):
        with self.assertRaises(TypeError):
            Reservation.objects.create(
                rental_id=self.rental.id,
                checkin=date("hey", 10, 10),
                checkout=date(1999, 10, 12),
            )
        self.assertEqual(Reservation.objects.count(), 0)

    def test_reservation_rental_id_invalid(self):
        with self.assertRaises(ValidationError) as exc:
            Reservation.objects.create(
                rental_id=5,
                checkin=date(1999, 10, 10),
                checkout=date(1999, 10, 12),
            )
        self.assertIn(
            "Rental with id 5 does not exist",
            exc.exception.messages,
        )
        self.assertEqual(Reservation.objects.count(), 0)
