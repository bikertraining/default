from django.db import models


class Ecourse(models.Model):
    link_3wbrc = models.URLField(
        blank=False,
        null=False
    )

    link_brc = models.URLField(
        blank=False,
        null=False
    )

    link_src = models.URLField(
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'ecourse'

        default_permissions = ()

        verbose_name = 'eCourse'
        verbose_name_plural = 'eCourse'
