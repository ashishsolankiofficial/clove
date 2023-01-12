from django.contrib import admin
from team.models import Team


class TeamAdmin(admin.ModelAdmin):
    exclude = ['ext_id', ]
    list_display = ["name", "country"]


admin.site.register(Team, TeamAdmin)
