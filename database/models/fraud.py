from django.db import models


class Fraud(models.Model):
    class FraudType(models.TextChoices):
        CCN = 'ccn', 'Credit Card Number'
        EMAIL = 'email', 'Email Address'
        GENERAL = 'general', 'General'
        IPADDRESS = 'ipaddress', 'IP Address'

    fraud_type = models.CharField(
        blank=False,
        choices=FraudType.choices,
        max_length=9,
        null=False
    )

    is_active = models.BooleanField(
        default=True
    )

    name = models.CharField(
        blank=False,
        null=False,
        unique=True
    )

    class Meta:
        db_table = 'fraud'

        default_permissions = ()

        verbose_name = 'Fraud String'
        verbose_name_plural = 'Fraud Strings'

    def __str__(self):
        return self.name
