# Generated by Django 5.1.4 on 2024-12-11 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0006_manager_alter_archivedtenant_sector_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sectors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector', models.CharField(blank=True, choices=[('الأمن العام - الشرطة', 'الأمن العام - الشرطة'), ('الأمن العام - المرور', 'الأمن العام - المرور'), ('الأمن العام - الدوريات الأمنية', 'الأمن العام - الدوريات الأمنية'), ('المباحث', 'المباحث'), ('الطوارئ الخاصة', 'الطوارئ الخاصة'), ('المخدرات', 'المخدرات'), ('الجوازات', 'الجوازات'), ('الدفاع المدني', 'الدفاع المدني'), ('السجون', 'السجون'), ('المجاهدين', 'المجاهدين'), ('حرس الحدود', 'حرس الحدود'), ('أمن المنشآت', 'أمن المنشآت'), ('الافواج الأمنية', 'الافواج الأمنية')], max_length=255, null=True)),
                ('major_villas', models.PositiveIntegerField(default=0)),
                ('minor_villas', models.PositiveIntegerField(default=0)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='manager',
            name='sector',
            field=models.CharField(blank=True, choices=[('الأمن العام - الشرطة', 'الأمن العام - الشرطة'), ('الأمن العام - المرور', 'الأمن العام - المرور'), ('الأمن العام - الدوريات الأمنية', 'الأمن العام - الدوريات الأمنية'), ('المباحث', 'المباحث'), ('الطوارئ الخاصة', 'الطوارئ الخاصة'), ('المخدرات', 'المخدرات'), ('الجوازات', 'الجوازات'), ('الدفاع المدني', 'الدفاع المدني'), ('السجون', 'السجون'), ('المجاهدين', 'المجاهدين'), ('حرس الحدود', 'حرس الحدود'), ('أمن المنشآت', 'أمن المنشآت'), ('الافواج الأمنية', 'الافواج الأمنية'), ('البلدية', 'البلدية'), ('صندوق التنمية العقارية', 'صندوق التنمية العقارية'), ('شركة الكهرباء', 'شركة الكهرباء')], max_length=255, null=True),
        ),
    ]
