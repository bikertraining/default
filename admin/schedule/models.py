from database import models


class Price(models.Price):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Admin Price'
        verbose_name_plural = 'Admin Prices'


class Register(models.Register):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Admin Register'
        verbose_name_plural = 'Admin Registrations'


class Schedule(models.Schedule):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Admin Schedule'
        verbose_name_plural = 'Admin Schedules'
