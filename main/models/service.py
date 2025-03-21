from django.db import models
from default.models import Service as ServiceType
from . import Renovation
from django.utils import translation
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Service(models.Model):
    service_type = models.ForeignKey(
        ServiceType,
        on_delete=models.PROTECT,
        null=True,
        related_name="services",
        verbose_name = _("Service")
    )

    renovation = models.OneToOneField(
        Renovation,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="service",
        verbose_name=_("Renovation")
    )

    def save(self, *args, **kwargs):
        from . import Stage
        is_new = self._state.adding
        super().save(*args, **kwargs) 

        if is_new and self.service_type:
            default_stages = self.service_type.stages.all()

            for default_stage in default_stages:
                stage = Stage.objects.create(service=self, name=default_stage.name)

                current_language = translation.get_language()

                try:
                    for lang_code, lang_name in settings.LANGUAGES:
                        translation.activate(lang_code)
                        setattr(stage, f'name_{lang_code}', default_stage.name)
                    stage.save()
                finally:
                    translation.activate(current_language)

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services") 

    def __str__(self):
        return f"{self.service_type.name if self.service_type else _('Unknown')}"