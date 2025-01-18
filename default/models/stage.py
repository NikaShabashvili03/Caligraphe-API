from django.db import models
from .service import Service
from django.utils.translation import gettext_lazy as _

class Stage(models.Model):
    service = models.ManyToManyField(
        Service,
        related_name="stages",
        verbose_name = _("Service")
    )
    
    name = models.CharField(max_length=100, verbose_name=_('Name'))

    class Meta:
        verbose_name = _("Stage")
        verbose_name_plural = _("Stages")
    
    def __str__(self):
        service_names = ", ".join([service.name for service in self.service.all()])
        return f"{self.name} ({_('Services')}: {service_names})"