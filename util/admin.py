from django.contrib import admin
from util.models import Country


class CountryAdmin(admin.ModelAdmin):
    exclude = ('ext_id',)
    list_display = ('name',)


# Register the admin class with the associated model
admin.site.register(Country, CountryAdmin)
