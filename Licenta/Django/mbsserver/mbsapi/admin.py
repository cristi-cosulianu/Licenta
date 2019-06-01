from django.contrib import admin

# Register your models here.

from .models import Persons, Payments, Bills, BillsToPayments, PaymentsStatus, ImagePost

admin.site.register(Persons)
admin.site.register(Payments)
admin.site.register(Bills)
admin.site.register(BillsToPayments)
admin.site.register(PaymentsStatus)
admin.site.register(ImagePost)
