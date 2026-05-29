from django.core.exceptions import ValidationError

from database import models


class Coupon(models.Coupon):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Admin Coupon'
        verbose_name_plural = 'Admin Coupons'

    def clean(self):
        self.name = self.name.upper()

        if not self.pk and Coupon.objects.filter(name=self.name).exists():
            raise ValidationError({'name': 'Name already exists.'})


class Price(models.Price):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Admin Price'
        verbose_name_plural = 'Admin Prices'
