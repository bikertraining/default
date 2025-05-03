from django.db import models


class Coupon(models.Model):
    class ClassType(models.TextChoices):
        BRC = 'brc', 'Basic RiderCourse'
        IME = 'ime', 'Kickstart'
        PRIVATE = 'private', 'Private'
        SRC = 'src', 'Skilled RiderCourse'
        THREEWBRC = '3wbrc', '3-Wheel Basic RiderCourse'

    amount = models.DecimalField(
        blank=False,
        decimal_places=2,
        default=0.00,
        max_digits=10,
        null=False
    )

    class_type = models.CharField(
        blank=False,
        choices=ClassType.choices,
        max_length=7,
        null=False
    )

    is_active = models.BooleanField(
        default=True
    )

    name = models.CharField(
        blank=False,
        max_length=100,
        null=False,
        unique=True
    )

    one_time_use = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 'coupon'

        default_permissions = ()

        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'

    def __str__(self):
        return self.name
