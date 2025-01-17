from django.db import models
from django.utils.translation import gettext_lazy as _

class Work(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Name'))

    class Meta:
        verbose_name = _("Work")
        verbose_name_plural = _("Works")
    
    def __str__(self):
        return self.name