from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

#REGISTERED MODEL
admin.site.register(CustomUser)
admin.site.register(Admin)
admin.site.register(Staff)
admin.site.register(Customer)
admin.site.register(Gender)
admin.site.register(Stafftype)
admin.site.register(Customertype)

#UNREGISTERED MODEL
admin.site.unregister(Group)