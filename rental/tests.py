from django.forms import ValidationError
from django.test import TestCase, RequestFactory

from rental.views import ReservationsListView
from .models import Rental, Reservation
from datetime import date
from django.contrib.auth.models import AnonymousUser


class ReservationTestCase(TestCase):
    def setUp(self) -> None:
        self.rental = Rental.objects.create(name="Rental 1")
        Reservation.objects.create(
            rental_id=self.rental.id,
            checkin=date(1999, 12, 8),
            checkout=date(1999, 12, 14),
        )

    def test_reservation_OK(self):
        Reservation.objects.create(
            rental_id=self.rental.id,
            checkin=date(1999, 10, 10),
            checkout=date(1999, 10, 12),
        )
        self.assertEqual(Reservation.objects.count(), 2)

    def test_reservation_date_combination_invalid(self):
        # Test error raised when reservation periods are overlaping.
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
        # Test eror raised when reservation period includes the existing.
        with self.assertRaises(ValidationError) as exc:
            Reservation.objects.create(
                rental_id=self.rental.id,
                checkin=date(1999, 12, 6),
                checkout=date(1999, 12, 16),
            )
        self.assertIn(
            "Reservation for this rental within this period already exists",
            exc.exception.messages,
        )
        self.assertEqual(Reservation.objects.count(), 1)

    def test_reservation_date_format_invalid(self):
        with self.assertRaises(TypeError):
            Reservation.objects.create(
                rental_id=self.rental.id,
                checkin=date("hey", 10, 10),
                checkout=date(1999, 10, 12),
            )
        self.assertEqual(Reservation.objects.count(), 1)


class ReservationListTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.rental_1 = Rental.objects.create(name="rental 1")
        self.rental_2 = Rental.objects.create(name="rental 2")

        self.reservation_1 = Reservation.objects.create(
            rental_id=self.rental_1.id,
            checkin=date(2022, 4, 13),
            checkout=date(2022, 4, 18),
        )
        self.reservation_2 = Reservation.objects.create(
            rental_id=self.rental_1.id,
            checkin=date(2022, 4, 22),
            checkout=date(2022, 4, 24),
        )
        self.reservation_3 = Reservation.objects.create(
            rental_id=self.rental_1.id,
            checkin=date(2022, 4, 8),
            checkout=date(2022, 4, 12),
        )
        self.reservation_4 = Reservation.objects.create(
            rental_id=self.rental_2.id,
            checkin=date(2022, 3, 8),
            checkout=date(2022, 4, 29),
        )
        self.reservation_5 = Reservation.objects.create(
            rental_id=self.rental_2.id,
            checkin=date(2022, 5, 8),
            checkout=date(2022, 5, 10),
        )

    def test_reservation_list_queryset(self):
        request = self.factory.get("")
        request.user = AnonymousUser()
        response = ReservationsListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        reservation_list = response.render().context_data["reservation_list"]
        print(reservation_list[0].rental_name)

        # Test queryset items ordered by checkin time.
        self.assertEqual(reservation_list[0], self.reservation_4)
        self.assertEqual(reservation_list[1], self.reservation_3)
        self.assertEqual(reservation_list[2], self.reservation_1)
        self.assertEqual(reservation_list[3], self.reservation_2)
        self.assertEqual(reservation_list[4], self.reservation_5)

        # Test item contains reference to previous item or None if earliest for the relevant rental.
        self.assertEqual(reservation_list[0].previous, None)
        self.assertEqual(reservation_list[1].previous, None)
        self.assertEqual(reservation_list[2].previous, self.reservation_3.id)
        self.assertEqual(reservation_list[3].previous, self.reservation_1.id)
        self.assertEqual(reservation_list[4].previous, self.reservation_4.id)
