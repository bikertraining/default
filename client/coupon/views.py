from django import views
from django.http import JsonResponse

from client.coupon import models


class Index(views.View):
    """
    Client - Coupon - Index
    """

    def get(self, request, **kwargs):
        try:
            result = models.Coupon.objects.get(
                class_type=self.kwargs.get('class_type', 'none').lower(),
                is_active=True,
                name=self.kwargs.get('name', 'none').upper()
            )

            data = {
                'amount': result.amount,
                'class_type': result.class_type,
                'is_active': result.is_active,
                'name': result.name
            }
        except models.Coupon.DoesNotExist:
            data = {
                'amount': '0.00',
                'class_type': '',
                'is_active': False,
                'name': ''
            }

        return JsonResponse(data, status=200)
