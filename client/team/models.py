from database import models


class Fraud(models.Fraud):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Client Fraud'
        verbose_name_plural = 'Client Fraud'
