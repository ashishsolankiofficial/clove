from django.contrib import admin
from payable.models import PayableProfile, BilateralBet, UnsettledBet

# Register your models here.


class PayableProfileAdmin(admin.ModelAdmin):
    exclude = ('ext_id',)


class BilateralBetAdmin(admin.ModelAdmin):
    exclude = ('ext_id',)


class UnsettledBetAdmin(admin.ModelAdmin):
    exclude = ('ext_id',)


admin.site.register(PayableProfile, PayableProfileAdmin)
admin.site.register(BilateralBet, BilateralBetAdmin)
admin.site.register(UnsettledBet, UnsettledBetAdmin)
