from django.db import models
from datetime import date

class Property(models.Model):
    FLOORS_CHOICES = [
        ('طابقين', 'طابقين'),
        ('3 طوابق', '3 طوابق'),
    ]

    TYPE_CHOICES = [
        ('للضباط', 'مخصصة للضباط'),
        ('للافراد', 'مخصصة للافراد'),
    ]
    SECTOR_CHOICES = [
        ('الأمن العام - الشرطة', 'الأمن العام - الشرطة'),
        ('الأمن العام - المرور', 'الأمن العام - المرور'),
        ('الأمن العام - الدوريات الأمنية', 'الأمن العام - الدوريات الأمنية'),
        ('المباحث', 'المباحث'),
        ('الطوارئ الخاصة', 'الطوارئ الخاصة'),
        ('المخدرات', 'المخدرات'),
        ('الجوازات', 'الجوازات'),
        ('الدفاع المدني', 'الدفاع المدني'),
        ('السجون', 'السجون'),
        ('المجاهدين', 'المجاهدين'),
        ('حرس الحدود', 'حرس الحدود'),
        ('أمن المنشآت', 'أمن المنشآت'),
        ('الافواج الأمنية', 'الافواج الأمنية'),
    ]
    cluster = models.CharField(max_length=50, null=True, blank=True)
    villa = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, default='شاغرة', null=True, blank=True)
    floors = models.CharField(max_length=10, choices=FLOORS_CHOICES, null=True, blank=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, null=True, blank=True)
    sector = models.CharField(max_length=255, choices=SECTOR_CHOICES, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cluster} - {self.villa}"

    def is_vacant(self):
        return self.status == 'شاغرة'

class Tenant(models.Model):
    SECTOR_CHOICES = [
        ('الأمن العام - الشرطة', 'الأمن العام - الشرطة'),
        ('الأمن العام - المرور', 'الأمن العام - المرور'),
        ('الأمن العام - الدوريات الأمنية', 'الأمن العام - الدوريات الأمنية'),
        ('المباحث', 'المباحث'),
        ('الطوارئ الخاصة', 'الطوارئ الخاصة'),
        ('المخدرات', 'المخدرات'),
        ('الجوازات', 'الجوازات'),
        ('الدفاع المدني', 'الدفاع المدني'),
        ('السجون', 'السجون'),
        ('المجاهدين', 'المجاهدين'),
        ('حرس الحدود', 'حرس الحدود'),
        ('أمن المنشآت', 'أمن المنشآت'),
        ('الافواج الأمنية', 'الافواج الأمنية'),
    ]

    name = models.CharField(max_length=255, null=True, blank=True)
    tenant_id = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    sector = models.CharField(max_length=255, choices=SECTOR_CHOICES, null=True, blank=True)
    date_of_lease = models.DateField(default=date.today, null=True, blank=True)
    rank = models.CharField(max_length=255, null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ArchivedTenant(models.Model):
    SECTOR_CHOICES = [
        ('الأمن العام - الشرطة', 'الأمن العام - الشرطة'),
        ('الأمن العام - المرور', 'الأمن العام - المرور'),
        ('الأمن العام - الدوريات الأمنية', 'الأمن العام - الدوريات الأمنية'),
        ('المباحث', 'المباحث'),
        ('الطوارئ الخاصة', 'الطوارئ الخاصة'),
        ('المخدرات', 'المخدرات'),
        ('الجوازات', 'الجوازات'),
        ('الدفاع المدني', 'الدفاع المدني'),
        ('السجون', 'السجون'),
        ('المجاهدين', 'المجاهدين'),
        ('حرس الحدود', 'حرس الحدود'),
        ('أمن المنشآت', 'أمن المنشآت'),
        ('الافواج الأمنية', 'الافواج الأمنية'),
    ]

    name = models.CharField(max_length=255, null=True, blank=True)
    tenant_id = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    sector = models.CharField(max_length=255, choices=SECTOR_CHOICES, null=True, blank=True)
    date_of_lease = models.DateField(null=True, blank=True)
    rank = models.CharField(max_length=50, null=True, blank=True)
    cluster = models.CharField(max_length=50, null=True, blank=True)
    villa = models.CharField(max_length=50, null=True, blank=True)
    archived_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
from django.db import models

class Manager(models.Model):
    SECTOR_CHOICES = [
        ('الأمن العام - الشرطة', 'الأمن العام - الشرطة'),
        ('الأمن العام - المرور', 'الأمن العام - المرور'),
        ('الأمن العام - الدوريات الأمنية', 'الأمن العام - الدوريات الأمنية'),
        ('المباحث', 'المباحث'),
        ('الطوارئ الخاصة', 'الطوارئ الخاصة'),
        ('المخدرات', 'المخدرات'),
        ('الجوازات', 'الجوازات'),
        ('الدفاع المدني', 'الدفاع المدني'),
        ('السجون', 'السجون'),
        ('المجاهدين', 'المجاهدين'),
        ('حرس الحدود', 'حرس الحدود'),
        ('أمن المنشآت', 'أمن المنشآت'),
        ('الافواج الأمنية', 'الافواج الأمنية'),
        ('البلدية', 'البلدية'),
        ('صندوق التنمية العقارية', 'صندوق التنمية العقارية'),
        ('شركة الكهرباء', 'شركة الكهرباء'),
    ]
    name = models.CharField(max_length=100)
    sector = models.CharField(max_length=255, choices=SECTOR_CHOICES, null=True, blank=True)
    rank = models.CharField(max_length=100)
    last_update = models.DateTimeField(auto_now=True)

def __str__(self):
        return self.name
    