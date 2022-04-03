from django.core.exceptions import ValidationError
import datetime
import re
from django.apps import apps


def validate_date(date_val):
    date_str = date_val.isoformat()
    pattern = re.compile(
        "^[0-2][0-9][0-9][0-9]-((0[1-9])|(1[0-2]))-(0[1-9]|[1-2][0-9]|3[0-1])$"
    )
    match = pattern.match(date_str)
    if not match:
        raise ValidationError(
            f"{date_str} is not a valid date in the YYYY-MM-DD format"
        )


def validate_id(id):
    Rental = apps.get_model("rental", "Rental")
    if not Rental.objects.filter(id=id).exists():
        raise ValidationError(f"Rental with id {id} does not exist")
