import random
import string
from django.db import models
from authentication.models.supervisor import Supervisor
from authentication.models.customer import Customer
from django.utils.translation import gettext_lazy as _

def generate_random_string(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class Renovation(models.Model):
    track = models.CharField(
        max_length=16, 
        default=generate_random_string,
        editable=False,
        verbose_name = _("Track")
    )
    
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, verbose_name=_('Supervisor'))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('Customer'))

    address = models.CharField(max_length=255, verbose_name=_('Address'))
    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(blank=True, null=True, verbose_name=_('End Date'))

    @property
    def progress(self):
        from main.models.service import Service
        
        try:
            service = self.service
        except Service.DoesNotExist:
            return 0.0

        stages = service.stages.all()
        completed_stages = sum(1 for stage in stages if stage.is_completed)
        total_stages = stages.count()

        return round((completed_stages / total_stages) * 100, 2) if total_stages > 0 else 0.0
    
    class Meta:
        verbose_name = _("Renovation")
        verbose_name_plural = _("Renovations")

    def __str__(self):
         return f"{self.id} | ({self.progress}%) | {self.address} | {self.track} ({self.start_date} / {self.end_date})"
    