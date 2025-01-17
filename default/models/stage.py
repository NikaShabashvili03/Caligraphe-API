from django.db import models
from .work import Work
from django.utils.translation import gettext_lazy as _

class Stage(models.Model):
    work = models.ManyToManyField(
        Work,
        related_name="stages",
        verbose_name = _("Work")
    )
    
    name = models.CharField(max_length=100, verbose_name=_('Name'))

    class Meta:
        verbose_name = _("Stage")
        verbose_name_plural = _("Stages")
    
    def __str__(self):
        work_names = ", ".join([work.name for work in self.work.all()])
        return f"{self.name} ({_('Works')}: {work_names})"