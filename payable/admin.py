from django.contrib import admin
from payable.models import PayableProfile

# Register your models here.


class PayableProfileAdmin(admin.ModelAdmin):
    exclude = ('ext_id',)


admin.site.register(PayableProfile, PayableProfileAdmin)
