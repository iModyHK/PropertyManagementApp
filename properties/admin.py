# myapp/admin.py
from django.contrib import admin
from .models import Property, Tenant, ArchivedTenant, Manager

admin.site.register(Property)
admin.site.register(Tenant)
admin.site.register(ArchivedTenant)
admin.site.register(Manager)