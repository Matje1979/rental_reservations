# Generated by Django 4.0.3 on 2022-04-03 16:25

from django.db import migrations, models
import rental.validators


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0002_alter_reservation_rental_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='checkin',
            field=models.DateField(validators=[rental.validators.validate_date]),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='checkout',
            field=models.DateField(validators=[rental.validators.validate_date]),
        ),
    ]
