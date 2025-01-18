from django.contrib import admin
from .models import Supervisor, Renovation, Stage, Service, StageImage
import os
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db.models import F

class StageInline(admin.TabularInline): 
    model = Stage
    extra = 1
    fields = ('name', 'is_completed')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by(F('is_completed').asc(nulls_last=True))
    
    def has_change_permission(self, request, obj=None):
        return False

class RenovationAdmin(admin.ModelAdmin):
    list_display = (
        'track', 
        'progress', 
        'supervisor', 
        'address', 
        'start_date', 
        'end_date', 
        'service_link',
        'copy_link'
    )

    def service_link(self, obj):
        if obj.service:
            url = reverse('admin:main_service_change', args=[obj.service.id]) 
            return format_html('<a href="{}">{}</a>', url, obj.service.service_type.name)
        return _("No Service Assigned")
    service_link.short_description = _('Service')

    def copy_link(self, obj):
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000") 
        url = f"{frontend_url}/track/{obj.track}"
        return format_html(
            '<button style="border: 0; padding: 2px 15px; cursor: pointer; border-radius: 50px; background: gray; color: white" type="button" class="btn btn-primary" onclick="copyToClipboard(\'{}\')">Copy Link</button>',
            url
        )
    copy_link.short_description = _('Copy Link')

    def progress(self, obj):
        return f"{obj.progress:.2f}%"
    progress.short_description = _('Progress')

    class Media:
        js = ('admin/js/copy_link.js',)

admin.site.register(Renovation, RenovationAdmin)

# Supervisor Admin
admin.site.register(Supervisor)


# Stage Admin
admin.site.register(StageImage)
admin.site.register(Stage)

# Service Admin
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_type', 'renovation')
    inlines = [StageInline]

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
