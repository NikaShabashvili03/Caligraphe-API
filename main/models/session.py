from . import Supervisor
from django.db import models
from django.utils.translation import gettext_lazy as _

class Session(models.Model):
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, verbose_name=_('Supervisor'))
    session_token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
          verbose_name = _("Session")
          verbose_name_plural = _("Sessions")

    def is_valid(self):
         return f"{self.supervisor.email} - {self.session_token}"
    
    def __str__(self):
         return f"{self.supervisor.firstname} | {self.created_at} / {self.expires_at}"