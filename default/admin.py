from django.contrib import admin
from .models import Stage, Service
from django.apps import apps
from django.utils.translation import gettext_lazy as _

def update_app_label_for_admin():
    default_app = apps.get_app_config('default')

    default_app.verbose_name = _("Default")

update_app_label_for_admin()
admin.site.register(Service)
admin.site.register(Stage)