from .customer import Customer
from .supervisor import Supervisor
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class Session(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('User'))
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Supervisor'))
    session_token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
          verbose_name = _("Session")
          verbose_name_plural = _("Sessions")

    def clean(self):
          if not self.customer and not self.supervisor:
               raise ValidationError(_("Either a customer or a supervisor must be set."))
          if self.customer and self.supervisor:
               raise ValidationError(_("A session can only have a customer or a supervisor, not both."))
          
    def is_valid(self):
         return f"{self.session_token}"
    
    def __str__(self):
         return f"{self.created_at} / {self.expires_at}"