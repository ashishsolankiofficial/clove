from django.contrib import admin
from playable.models import Sport, Tournament, BilateralMatch


class SportAdmin(admin.ModelAdmin):
    exclude = ('ext_id',)
    list_display = ('name',)


class TournamentAdmin(admin.ModelAdmin):
    exclude = ('ext_id',)


class BilateralMatchAdmin(admin.ModelAdmin):
    exclude = ('ext_id',)


admin.site.register(Sport, SportAdmin)
admin.site.register(Tournament, TournamentAdmin)
# # admin.site.register(BilateralMatch, BilateralMatchAdmin)
