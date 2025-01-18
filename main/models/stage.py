from django.db import models
from . import Service
from django.utils.translation import gettext_lazy as _
from ..utils import image_upload, validate_image

def upload_image(instance, filename):
    return image_upload(instance, filename, 'stages/')

class Stage(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="stages",
        verbose_name = _("Service")
    )

    name = models.CharField(max_length=100, verbose_name=_('Name'))
    is_completed = models.DateTimeField(null=True, blank=True, default=None, verbose_name=_('Is Complited'))
    
    class Meta:
        verbose_name = _("Stage")
        verbose_name_plural = _("Stages")
    
    def __str__(self):
        return f"{self.name} ({_('Is Complited') if self.is_completed else _('Not Completed')})"
    

class StageImage(models.Model):
    stage = models.ForeignKey(Stage, related_name='images', on_delete=models.CASCADE, verbose_name = _("Stage"))
    url = models.ImageField(upload_to=upload_image, null=True, blank=True, verbose_name=_('Url'))

    class Meta:
        verbose_name = _("Stage Image")
        verbose_name_plural = _("Stage Images")
        
    def clean(self):
        if self.url:
            validate_image(self.url, 4000, 4000, 4000)

    def __str__(self):
        return f"{self.stage.service.service_type.name} | {self.stage.name}"