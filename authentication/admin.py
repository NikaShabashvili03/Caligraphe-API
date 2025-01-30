from django.contrib import admin
from .models import Customer, Session, Supervisor
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken, EmailAddress
from django.contrib.sites.models import Site
from django.apps import apps
from django.utils.translation import gettext_lazy as _

def update_app_label_for_admin():
    authentication_app = apps.get_app_config('authentication')

    authentication_app.verbose_name = _("Authentication")

update_app_label_for_admin()

    
admin.site.register(Customer)
admin.site.register(Session)
admin.site.register(Supervisor)


admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
admin.site.unregister(Site)
admin.site.unregister(EmailAddress)