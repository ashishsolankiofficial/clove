from django.contrib import admin
from payable.models import PayableProfile, OfficeBet, UnsettledBet

# Register your models here.


class PayableProfileAdmin(admin.ModelAdmin):
    exclude = ('ext_id',)


class OfficeBetAdmin(admin.ModelAdmin):
    exclude = ('ext_id',)


class UnsettledBetAdmin(admin.ModelAdmin):
    exclude = ('ext_id',)


admin.site.register(PayableProfile, PayableProfileAdmin)
admin.site.register(OfficeBet, OfficeBetAdmin)
admin.site.register(UnsettledBet, UnsettledBetAdmin)
