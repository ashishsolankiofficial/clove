from django.contrib import admin
from office.models import Office


class OfficeAdmin(admin.ModelAdmin):
    fields = ("name", "address")
    list_display = ('name', 'address')
    pass


# Register the admin class with the associated model
admin.site.register(Office, OfficeAdmin)
