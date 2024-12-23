import csv
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Max, Sum
from .models import Property, Tenant, ArchivedTenant  # Assuming you have a Form model
from .forms import PropertyForm, TenantForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from datetime import date  # Import date
from weasyprint import HTML
from django.template.loader import render_to_string
from datetime import datetime
import logging
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)

@login_required
def property_list(request):
    query = request.GET.get('q')
    column = request.GET.get('column')
    if query and column:
        if column == 'حي':
            properties = Property.objects.filter(cluster__icontains=query)
        elif column == 'وحدة':
            properties = Property.objects.filter(villa__icontains=query)
        elif column == 'حالة':
            properties = Property.objects.filter(status__icontains=query)
        elif column == 'طوابق':
            properties = Property.objects.filter(floors__icontains=query)
        elif column == 'نوع':
            properties = Property.objects.filter(type__icontains=query)
        elif column == 'قطاع':
            properties = Property.objects.filter(sector__icontains=query)
    else:
        properties = Property.objects.all()
    
    context = {
        'properties': properties,
        'last_update': Property.objects.latest('updated_at').updated_at,
    }
    return render(request, 'properties/property_list.html', context)

@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('property_list')
    else:
        form = PropertyForm()
    return render(request, 'properties/property_form.html', {'form': form})

@login_required
def property_edit(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return redirect('property_list')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'properties/property_form.html', {'form': form})

@login_required
def property_delete(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property.delete()
        return redirect('property_list')
    return render(request, 'properties/property_confirm_delete.html', {'property': property})

@login_required
def tenant_list(request):
    query = request.GET.get('q', '')
    column = request.GET.get('column', '')
    if query and column:
        if column == 'name':
            tenants = Tenant.objects.filter(name__icontains=query)
        elif column == 'tenant_id':
            tenants = Tenant.objects.filter(tenant_id__icontains=query)
        elif column == 'mobile':
            tenants = Tenant.objects.filter(mobile__icontains=query)
        elif column == 'sector':
            tenants = Tenant.objects.filter(sector__icontains=query)
        elif column == 'rank':
            tenants = Tenant.objects.filter(rank__icontains=query)
        elif column == 'property__cluster':
            tenants = Tenant.objects.filter(property__cluster__icontains=query)
        elif column == 'property__villa':
            tenants = Tenant.objects.filter(property__villa__icontains=query)
    else:
        tenants = Tenant.objects.all()
    
    context = {
        'tenants': tenants,
        'last_update': tenants.aggregate(last_update=Max('updated_at'))['last_update'],
    }
    return render(request, 'tenants/tenant_list.html', context)

@login_required
def tenant_create(request):
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            tenant = form.save()
            tenant.property.status = 'مشغولة'
            tenant.property.save()
            return redirect('tenant_list')
    else:
        form = TenantForm()
    return render(request, 'tenants/tenant_form.html', {'form': form})

@login_required
def tenant_edit(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if request.method == 'POST':
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm(instance=tenant)
    return render(request, 'tenants/tenant_form.html', {'form': form})

@login_required
def tenant_delete(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if request.method == 'POST':
        # Archive the tenant data with the current date
        ArchivedTenant.objects.create(
            name=tenant.name,
            tenant_id=tenant.tenant_id,
            mobile=tenant.mobile,
            sector=tenant.sector,
            date_of_lease=tenant.date_of_lease,
            rank=tenant.rank,
            cluster=tenant.property.cluster,
            villa=tenant.property.villa,
            archived_date=date.today()  # Set the archived date to today
        )
        tenant.property.status = 'شاغرة'
        tenant.property.save()
        tenant.delete()
        return redirect('tenant_list')
    return render(request, 'tenants/tenant_confirm_delete.html', {'tenant': tenant})

@login_required
def archived_tenant_list(request):
    archived_tenants = ArchivedTenant.objects.all()
    last_update = archived_tenants.aggregate(last_update=Max('archived_date'))['last_update']
    return render(request, 'tenants/archived_tenant_list.html', {'archived_tenants': archived_tenants, 'last_update': last_update})

@login_required
def unarchive_tenant(request, pk):
    archived_tenant = get_object_or_404(ArchivedTenant, pk=pk)
    property = Property.objects.filter(cluster=archived_tenant.cluster, villa=archived_tenant.villa).first()
    if property:
        property.status = 'مشغولة'
        property.save()
        Tenant.objects.create(
            name=archived_tenant.name,
            tenant_id=archived_tenant.tenant_id,
            mobile=archived_tenant.mobile,
            sector=archived_tenant.sector,
            date_of_lease=archived_tenant.date_of_lease,
            rank=archived_tenant.rank,
            property=property
        )
        archived_tenant.delete()
    return redirect('archived_tenant_list')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('property_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('')
        else:
            return render(request, 'registration/login.html', {'خطأ': 'اسم المستخدم أو كلمة المرور غير صحيحة'})
    return render(request, 'registration/login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login_view')  # Redirect to the login page after logging out
    return redirect('property_list')  # Redirect to the login page after logging out

@login_required
def export_properties_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="properties.csv"'

    writer = csv.writer(response)
    writer.writerow(['Cluster', 'Villa', 'Status', 'Floors', 'Type'])

    properties = Property.objects.all().values_list('cluster', 'villa', 'status', 'floors', 'type')
    for property in properties:
        writer.writerow(property)

    return response

@login_required
def export_tenants_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tenants.csv"'

    writer = csv.writer(response)
    writer.writerow(['الاسم', 'رقم السجل المدني', 'رقم الجوال', 'القطاع', 'تاريخ استلام الوحدة', 'الرتبة', 'الحي', 'الوحدة'])

    tenants = Tenant.objects.all().values_list('name', 'tenant_id', 'mobile', 'sector', 'date_of_lease', 'rank', 'property__cluster', 'property__villa')
    for tenant in tenants:
        writer.writerow(tenant)

    return response

@login_required
def export_properties_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="properties.xlsx"'

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Properties'

    columns = ['Cluster', 'Villa', 'Status', 'Floors', 'Type']
    row_num = 1

    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title

    properties = Property.objects.all().values_list('cluster', 'villa', 'status', 'floors', 'type')
    for property in properties:
        row_num += 1
        for col_num, cell_value in enumerate(property, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value

    workbook.save(response)
    return response

@login_required
def export_tenants_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="tenants.xlsx"'

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Tenants'

    columns = ['Name', 'ID', 'Mobile', 'Sector', 'Date of Lease', 'Rank', 'Cluster', 'Villa']
    row_num = 1

    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title

    tenants = Tenant.objects.all().values_list('name', 'tenant_id', 'mobile', 'sector', 'date_of_lease', 'rank', 'property__cluster', 'property__villa')
    for tenant in tenants:
        row_num += 1
        for col_num, cell_value in enumerate(tenant, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value

    workbook.save(response)
    return response

@login_required
def export_archived_tenants_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="archived_tenants.xlsx"'

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Archived Tenants'

    columns = ['Name', 'ID', 'Mobile', 'Sector', 'Date of Lease', 'Rank', 'Cluster', 'Villa', 'Archived Date']
    row_num = 1

    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title

    archived_tenants = ArchivedTenant.objects.all().values_list('name', 'tenant_id', 'mobile', 'sector', 'date_of_lease', 'rank', 'cluster', 'villa', 'archived_date')
    for archived_tenant in archived_tenants:
        row_num += 1
        for col_num, cell_value in enumerate(archived_tenant, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value

    workbook.save(response)
    return response

from django.db.models import Count

from django.db.models import Count

from django.db.models import Count

@login_required
def dashboard(request):
    occupied_count = Property.objects.filter(status='مشغولة').count()
    vacant_count = Property.objects.filter(status='شاغرة').count()

    # Count tenants and properties based on sector and type
    tenants_by_sector_and_type = Tenant.objects.values('property__sector', 'property__type').annotate(tenant_count=Count('id'))
    properties_by_sector_and_type = Property.objects.values('sector', 'type').annotate(property_count=Count('id'))

    # Aggregate data by sector
    sectors = {}
    for tenant in tenants_by_sector_and_type:
        sector = tenant['property__sector']
        type_ = tenant['property__type']
        if sector not in sectors:
            sectors[sector] = {'total_tenants': 0, 'total_properties': 0, 'types': {}}
        if type_ not in sectors[sector]['types']:
            sectors[sector]['types'][type_] = {'tenant_count': tenant['tenant_count'], 'property_count': 0}
        else:
            sectors[sector]['types'][type_]['tenant_count'] += tenant['tenant_count']
        sectors[sector]['total_tenants'] += tenant['tenant_count']

    for property_ in properties_by_sector_and_type:
        sector = property_['sector']
        type_ = property_['type']
        if sector not in sectors:
            sectors[sector] = {'total_tenants': 0, 'total_properties': 0, 'types': {}}
        if type_ not in sectors[sector]['types']:
            sectors[sector]['types'][type_] = {'tenant_count': 0, 'property_count': property_['property_count']}
        else:
            sectors[sector]['types'][type_]['property_count'] += property_['property_count']
        sectors[sector]['total_properties'] += property_['property_count']

    context = {
        'occupied_count': occupied_count,
        'vacant_count': vacant_count,
        'sectors': sectors,
    }
    return render(request, 'dashboard.html', context)


@login_required
def print_properties_pdf(request):
    properties = Property.objects.all()
    last_update = properties.aggregate(last_update=Max('updated_at'))['last_update']
    html_string = render_to_string('properties/property_list_pdf.html', {'properties': properties, 'last_update': last_update})
    html = HTML(string=html_string)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=properties.pdf'
    html.write_pdf(response)
    return response

@login_required
def print_tenants_pdf(request):
    tenants = Tenant.objects.all()
    last_update = tenants.aggregate(last_update=Max('updated_at'))['last_update']
    html_string = render_to_string('tenants/tenant_list_pdf.html', {'tenants': tenants, 'last_update': last_update})
    html = HTML(string=html_string)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=tenants.pdf'
    html.write_pdf(response)
    return response

@login_required
def print_archived_tenants_pdf(request):
    archived_tenants = ArchivedTenant.objects.all()
    last_update = archived_tenants.aggregate(last_update=Max('archived_date'))['last_update']
    html_string = render_to_string('tenants/archived_tenant_list_pdf.html', {'archived_tenants': archived_tenants, 'last_update': last_update})
    html = HTML(string=html_string)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=archived_tenants.pdf'
    html.write_pdf(response)
    return response

def my_view(request):
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
    # Your view logic here

@login_required
def export_tenants_pdf(request):
    if request.method == 'POST':
        selected_sectors = request.POST.getlist('sectors')
        
        # Filter tenants based on selected sectors
        tenants = Tenant.objects.filter(sector__in=selected_sectors).values_list(
            'name', 'tenant_id', 'mobile', 'sector', 'date_of_lease', 'rank', 'property__cluster', 'property__villa'
        )

        # Create PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.drawString(100, 750, "قائمة أسماء السكان الحاليين")

        y = 700
        for tenant in tenants:
            p.drawString(100, y, f"{tenant[0]}, {tenant[1]}, {tenant[2]}, {tenant[3]}, {tenant[4]}, {tenant[5]}, {tenant[6]}, {tenant[7]}")
            y -= 20

        p.showPage()
        p.save()

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    sectors = Tenant.objects.values_list('sector', flat=True).distinct()
    return render(request, 'tenant_list_pdf.html', {'sectors': sectors})

@login_required
def tenant_list_pdf(request):
    query = request.GET.get('q', '')
    column = request.GET.get('column', '')
    if query and column:
        if column == 'name':
            tenants = Tenant.objects.filter(name__icontains=query)
        elif column == 'tenant_id':
            tenants = Tenant.objects.filter(tenant_id__icontains=query)
        elif column == 'mobile':
            tenants = Tenant.objects.filter(mobile__icontains=query)
        elif column == 'sector':
            tenants = Tenant.objects.filter(sector__icontains=query)
        elif column == 'rank':
            tenants = Tenant.objects.filter(rank__icontains=query)
        elif column == 'property__cluster':
            tenants = Tenant.objects.filter(property__cluster__icontains=query)
        elif column == 'property__villa':
            tenants = Tenant.objects.filter(property__villa__icontains=query)
    else:
        tenants = Tenant.objects.all()
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "قائمة أسماء السكان الحاليين")

    y = 700
    for tenant in tenants:
        p.drawString(100, y, f"{tenant.name}, {tenant.tenant_id}, {tenant.mobile}, {tenant.sector}, {tenant.rank}, {tenant.property.cluster}, {tenant.property.villa}")
        y -= 20

    p.showPage()
    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="tenant_list.pdf"'
    
    context = {
        'tenants': tenants,
    }
    template_path = 'tenants/tenant_list_pdf.html'
    html_string = render_to_string(template_path, context)
    HTML(string=html_string).write_pdf(response)
    
    return response


from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.db.models import Q, Max
from django.contrib.auth.decorators import login_required

@login_required
def property_list_pdf(request):
    query = request.GET.get('q')
    column = request.GET.get('column')
    if query and column:
        if column == 'حي':
            properties = Property.objects.filter(cluster__icontains=query)
        elif column == 'وحدة':
            properties = Property.objects.filter(villa__icontains=query)
        elif column == 'حالة':
            properties = Property.objects.filter(status__icontains=query)
        elif column == 'طوابق':
            properties = Property.objects.filter(floors__icontains=query)
        elif column == 'نوع':
            properties = Property.objects.filter(type__icontains=query)
        elif column == 'قطاع':
            properties = Property.objects.filter(sector__icontains=query)
    else:
        properties = Property.objects.all()
    last_update = properties.aggregate(last_update=Max('updated_at'))['last_update']
    
    template_path = 'properties/property_list_pdf.html'
    context = {'properties': properties, 'last_update': last_update}
    html_string = render_to_string(template_path, context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="property_list.pdf"'
    
    HTML(string=html_string).write_pdf(response)
    
    return response

@login_required
def forms_list(request):
    forms = [
        {'name': 'استلام'},
        {'name': 'اخلاء'},
        {'name': 'تمديد'}
    ]
    return render(request, 'forms_pdf/forms_list.html', {'forms': forms})

from .models import Manager
from .forms import ManagerForm

def managers_list(request):
    managers = Manager.objects.all()
    return render(request, 'managers/managers_list.html', {'managers': managers})

def manager_create(request):
    if request.method == "POST":
        form = ManagerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('managers_list')
    else:
        form = ManagerForm()
    return render(request, 'managers/manager_form.html', {'form': form})

def manager_edit(request, pk):
    manager = get_object_or_404(Manager, pk=pk)
    if request.method == "POST":
        form = ManagerForm(request.POST, instance=manager)
        if form.is_valid():
            form.save()
            return redirect('managers_list')
    else:
        form = ManagerForm(instance=manager)
    return render(request, 'managers/manager_form.html', {'form': form})
