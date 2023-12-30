from django.contrib import admin
from django_task.admin import TaskAdmin

from .models import Domain, Serveur, CheckMailTaskThreaded

admin.site.register(Domain)
admin.site.register(Serveur)

@admin.register(CheckMailTaskThreaded)
class CheckMailTaskThreadedAdmin(TaskAdmin):

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        return list_display + ['serveur', ]