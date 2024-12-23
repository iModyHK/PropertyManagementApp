# Generated by Django 5.1.4 on 2024-12-09 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0005_property_updated_at_tenant_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sector', models.CharField(max_length=100)),
                ('rank', models.CharField(max_length=100)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='archivedtenant',
            name='sector',
            field=models.CharField(blank=True, choices=[('الأمن العام - الشرطة', 'الأمن العام - الشرطة'), ('الأمن العام - المرور', 'الأمن العام - المرور'), ('الأمن العام - الدوريات الأمنية', 'الأمن العام - الدوريات الأمنية'), ('المباحث', 'المباحث'), ('الطوارئ الخاصة', 'الطوارئ الخاصة'), ('المخدرات', 'المخدرات'), ('الجوازات', 'الجوازات'), ('الدفاع المدني', 'الدفاع المدني'), ('السجون', 'السجون'), ('المجاهدين', 'المجاهدين'), ('حرس الحدود', 'حرس الحدود'), ('أمن المنشآت', 'أمن المنشآت'), ('الافواج الأمنية', 'الافواج الأمنية')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='floors',
            field=models.CharField(blank=True, choices=[('طابقين', 'طابقين'), ('3 طوابق', '3 طوابق')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='status',
            field=models.CharField(blank=True, default='شاغرة', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='type',
            field=models.CharField(blank=True, choices=[('مخصصة للضباط', 'مخصصة للضباط'), ('مخصصة للافراد', 'مخصصة للافراد')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='mobile',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='rank',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='sector',
            field=models.CharField(blank=True, choices=[('الأمن العام - الشرطة', 'الأمن العام - الشرطة'), ('الأمن العام - المرور', 'الأمن العام - المرور'), ('الأمن العام - الدوريات الأمنية', 'الأمن العام - الدوريات الأمنية'), ('المباحث', 'المباحث'), ('الطوارئ الخاصة', 'الطوارئ الخاصة'), ('المخدرات', 'المخدرات'), ('الجوازات', 'الجوازات'), ('الدفاع المدني', 'الدفاع المدني'), ('السجون', 'السجون'), ('المجاهدين', 'المجاهدين'), ('حرس الحدود', 'حرس الحدود'), ('أمن المنشآت', 'أمن المنشآت'), ('الافواج الأمنية', 'الافواج الأمنية')], max_length=255, null=True),
        ),
    ]