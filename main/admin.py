from django.contrib import admin
from .models import Supervisor, Renovation, Stage, Service, StageImage
import os
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

class RenovationAdmin(admin.ModelAdmin):
    list_display = ('track', 'progress', 'supervisor', 'address', 'start_date', 'end_date', 'service_names', 'copy_link')

    def service_names(self, obj):
        return obj.service.service_type.name if obj.service else _("No Service Assigned")
    service_names.short_description = _('Service')

    def copy_link(self, obj):
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000") 
        url = f"{frontend_url}/track/{obj.track}"
        return format_html(
            '<button style="border: 0; padding: 2px 15px; cursor: pointer; border-radius: 50px; background: gray; color: white" type="button" class="btn btn-primary" onclick="copyToClipboard(\'{}\')">Copy Link</button>',
            url
        )
    copy_link.short_description = _('Copy Link')

    class Media:
        js = ('admin/js/copy_link.js',)

    def progress(self, obj):
        return f"{obj.progress:.2f}%"
    progress.short_description = _('Progress')

admin.site.register(Renovation, RenovationAdmin)

# Supervisor Admin
admin.site.register(Supervisor)


# Stage Admin
admin.site.register(StageImage)
admin.site.register(Stage)

# Service Admin
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_type', 'renovation')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'renovation':
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                try:
                    service = Service.objects.get(pk=obj_id)
                    if service.renovation: 
                        kwargs['queryset'] = Renovation.objects.filter(pk=service.renovation.pk)
                    else: 
                        kwargs['queryset'] = Renovation.objects.exclude(
                            id__in=Service.objects.values_list('renovation_id', flat=True)
                        )
                except Service.DoesNotExist:
                    pass
            else:
                kwargs['queryset'] = Renovation.objects.exclude(
                    id__in=Service.objects.values_list('renovation_id', flat=True)
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
admin.site.register(Service, ServiceAdmin)
