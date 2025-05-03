from database import models


class Coupon(models.Coupon):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Admin Coupon'
        verbose_name_plural = 'Admin Coupons'


class Price(models.Price):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Admin Price'
        verbose_name_plural = 'Admin Prices'
