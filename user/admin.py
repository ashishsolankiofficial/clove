from django.contrib import admin
from user.models import User


class UserAdmin(admin.ModelAdmin):
    exclude = ('ext_id',)
    list_display = ('display_name', 'first_name', 'last_name', 'office')
    pass


# Register the admin class with the associated model
admin.site.register(User, UserAdmin)
