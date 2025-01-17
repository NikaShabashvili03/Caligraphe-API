from django.contrib import admin
from .models import Supervisor, Renovation, Stage, Work, StageImage
import os
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

class RenovationAdmin(admin.ModelAdmin):
    list_display = ('track', 'progress', 'supervisor', 'address', 'start_date', 'end_date', 'work_names', 'copy_link')

    def work_names(self, obj):
        return obj.work.work_type.name if obj.work else _("No Work Assigned")
    work_names.short_description = _('Work')

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

# Work Admin
class WorkAdmin(admin.ModelAdmin):
    list_display = ('work_type', 'renovation')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'renovation':
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                try:
                    work = Work.objects.get(pk=obj_id)
                    if work.renovation: 
                        kwargs['queryset'] = Renovation.objects.filter(pk=work.renovation.pk)
                    else: 
                        kwargs['queryset'] = Renovation.objects.exclude(
                            id__in=Work.objects.values_list('renovation_id', flat=True)
                        )
                except Work.DoesNotExist:
                    pass
            else:
                kwargs['queryset'] = Renovation.objects.exclude(
                    id__in=Work.objects.values_list('renovation_id', flat=True)
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
admin.site.register(Work, WorkAdmin)
