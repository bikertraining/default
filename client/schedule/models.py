from database import models


class Schedule(models.Schedule):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Client Schedule'
        verbose_name_plural = 'Client Schedules'
