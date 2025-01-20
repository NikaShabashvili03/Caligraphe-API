from django.contrib import admin
from .models import Customer, Session, Supervisor

admin.site.register(Customer)
admin.site.register(Session)
admin.site.register(Supervisor)