from django import forms
from django.db import models
from .models import Property, Tenant, Manager

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['cluster', 'villa', 'status', 'floors', 'type', 'sector']
        labels = {
            'cluster': 'الحي',
            'villa': 'الوحدة',
            'status': 'الحالة',
            'floors': 'عدد الطوابق',
            'type': 'النوع',
            'sector': 'القطاع'
        }
        widgets = {
            'status': forms.HiddenInput(),  # Hide the status field in the form
        }

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'tenant_id', 'mobile', 'sector', 'date_of_lease', 'rank', 'property']
        labels = {
            'name': 'الاسم',
            'tenant_id': 'رقم السجل المدني',
            'mobile': 'رقم الجوال',
            'sector': 'القطاع',
            'date_of_lease': 'تاريخ استلام الوحدة',
            'rank': 'الرتبة',
            'property': 'الوحدة'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.property:
                self.fields['property'].queryset = Property.objects.filter(
                    models.Q(status='شاغرة') | models.Q(pk=self.instance.property.pk)
                )
            else:
                self.fields['property'].queryset = Property.objects.filter(status='شاغرة')
        else:
            self.fields['property'].queryset = Property.objects.filter(status='شاغرة')
            self.fields['date_of_lease'].widget = forms.DateInput(attrs={'type': 'date'})

class ManagerForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = ['name', 'sector', 'rank']
        labels = {
            'name': 'الاسم',
            'sector': 'القطاع / الجهة',
            'rank': 'الرتبة / المنصب',
        }
