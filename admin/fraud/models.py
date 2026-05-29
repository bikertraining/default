from django.core.exceptions import ValidationError

from database import models


class Fraud(models.Fraud):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Admin Fraud'
        verbose_name_plural = 'Admin Fraud'

    def clean(self):
        self.name = self.name.lower()

        if not self.pk and Fraud.objects.filter(name=self.name).exists():
            raise ValidationError({'name': 'Name already exists.'})
