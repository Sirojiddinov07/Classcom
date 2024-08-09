from django.contrib import admin
from .models import Plans, Payments, Orders
# Register your models here.


admin.site.register(Payments)
admin.site.register(Plans)
admin.site.register(Orders)
