from django.db import models


class Schedule(models.Model):
    class DayType(models.TextChoices):
        MONDAY_TUESDAY = 'monday_tuesday', 'Monday - Tuesday'
        THURSDAY_FRIDAY = 'thursday_friday', 'Thursday - Friday'
        SATURDAY_SUNDAY = 'saturday_sunday', 'Saturday - Sunday'
        SUNDAY_MONDAY = 'sunday_monday', 'Sunday - Monday'
        SUNDAY = 'sunday', 'Sunday'

    price = models.ForeignKey(
        'Price',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='schedule_price',
        verbose_name='Class'
    )

    date_from = models.DateField(
        auto_now_add=False,
    )

    date_to = models.DateField(
        auto_now_add=False
    )

    day_type = models.CharField(
        blank=False,
        choices=DayType.choices,
        max_length=16,
        null=False
    )

    seats = models.CharField(
        blank=False,
        default=12,
        max_length=2,
        null=False
    )

    class Meta:
        db_table = 'schedule'

        default_permissions = ()

        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'

    def __str__(self):
        return self.price.get_class_type_display()
