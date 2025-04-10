from django.shortcuts import render, redirect, get_object_or_404
from .models import CashFlow, Status, Type, Category, SubCategory
from .forms import CashFlowForm, CashFlowFilterForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

# Главная страница со списком записей
def cashflow_list(request):
    cashflows = CashFlow.objects.all()
    form = CashFlowFilterForm(request.GET)

    if form.is_valid():
        if form.cleaned_data['start_date']:
            cashflows = cashflows.filter(created_date__gte=form.cleaned_data['start_date'])
        if form.cleaned_data['end_date']:
            cashflows = cashflows.filter(created_date__lte=form.cleaned_data['end_date'])
        if form.cleaned_data['status']:
            cashflows = cashflows.filter(status=form.cleaned_data['status'])
        if form.cleaned_data['type']:
            cashflows = cashflows.filter(type=form.cleaned_data['type'])
        if form.cleaned_data['category']:
            cashflows = cashflows.filter(category=form.cleaned_data['category'])
        if form.cleaned_data['subcategory']:
            cashflows = cashflows.filter(subcategory=form.cleaned_data['subcategory'])

    return render(request, 'cashflow/cashflow_list.html', {'cashflows': cashflows, 'form': form})

# Создание записи
def cashflow_create(request):
    if request.method == 'POST':
        form = CashFlowForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'CashFlow entry created successfully.')
            return redirect('cashflow_list')
        else:
            messages.error(request, 'There was an error in your form. Please check the errors below.')
    else:
        form = CashFlowForm()
    
    return render(request, 'cashflow/cashflow_form.html', {'form': form})

# Редактирование записи
def cashflow_edit(request, pk):
    cashflow = get_object_or_404(CashFlow, pk=pk)
    if request.method == 'POST':
        form = CashFlowForm(request.POST, instance=cashflow)
        if form.is_valid():
            form.save()
            messages.success(request, 'CashFlow entry updated successfully.')
            return redirect('cashflow_list')
        else:
            messages.error(request, 'There was an error in your form. Please check the errors below.')
    else:
        form = CashFlowForm(instance=cashflow)
    
    return render(request, 'cashflow/cashflow_form.html', {'form': form})

# Удаление записи
def cashflow_delete(request, pk):
    cashflow = get_object_or_404(CashFlow, pk=pk)
    if request.method == 'POST':
        cashflow.delete()
        return redirect('cashflow_list')
    return render(request, 'cashflow/cashflow_confirm_delete.html', {'cashflow': cashflow})

# Управление справочниками (заглушка, реализуем позже)
def manage_directories(request):
    statuses = Status.objects.all()
    types = Type.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    return render(request, 'cashflow/manage_directories.html', {
        'statuses': statuses,
        'types': types,
        'categories': categories,
        'subcategories': subcategories
    })

def get_categories(request):
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

def get_all_categories(request):
    categories = Category.objects.all().values('id', 'name')
    return JsonResponse(list(categories), safe=False)

def get_all_subcategories(request):
    subcategories = SubCategory.objects.all().values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

# Status views
def status_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Status.objects.create(name=name)
        messages.success(request, 'Status created successfully.')
        return redirect('manage_directories')
    return render(request, 'cashflow/status_form.html')

def status_edit(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        status.name = request.POST.get('name')
        status.save()
        messages.success(request, 'Status updated successfully.')
        return redirect('manage_directories')
    return render(request, 'cashflow/status_form.html', {'status': status})

def status_delete(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        status.delete()
        messages.success(request, 'Status deleted successfully.')
        return redirect('manage_directories')
    return render(request, 'cashflow/status_confirm_delete.html', {'status': status})

# Type views
def type_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Type.objects.create(name=name)
        messages.success(request, 'Type created successfully.')
        return redirect('manage_directories')
    return render(request, 'cashflow/type_form.html')

def type_edit(request, pk):
    type_obj = get_object_or_404(Type, pk=pk)
    if request.method == 'POST':
        type_obj.name = request.POST.get('name')
        type_obj.save()
        messages.success(request, 'Type updated successfully.')
        return redirect('manage_directories')
    return render(request, 'cashflow/type_form.html', {'type': type_obj})

def type_delete(request, pk):
    type_obj = get_object_or_404(Type, pk=pk)
    if request.method == 'POST':
        type_obj.delete()
        messages.success(request, 'Type deleted successfully.')
        return redirect('manage_directories')
    return render(request, 'cashflow/type_confirm_delete.html', {'type': type_obj})

# Category views
def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        type_id = request.POST.get('type')
        type_obj = get_object_or_404(Type, pk=type_id)
        Category.objects.create(name=name, type=type_obj)
        messages.success(request, 'Category created successfully.')
        return redirect('manage_directories')
    types = Type.objects.all()
    return render(request, 'cashflow/category_form.html', {'types': types})

def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        type_id = request.POST.get('type')
        category.type = get_object_or_404(Type, pk=type_id)
        category.save()
        messages.success(request, 'Category updated successfully.')
        return redirect('manage_directories')
    types = Type.objects.all()
    return render(request, 'cashflow/category_form.html', {'category': category, 'types': types})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('manage_directories')
    return render(request, 'cashflow/category_confirm_delete.html', {'category': category})

# Subcategory views
def subcategory_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, pk=category_id)
        SubCategory.objects.create(name=name, category=category)
        messages.success(request, 'Subcategory created successfully.')
        return redirect('manage_directories')
    categories = Category.objects.all()
    return render(request, 'cashflow/subcategory_form.html', {'categories': categories})

def subcategory_edit(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    if request.method == 'POST':
        subcategory.name = request.POST.get('name')
        category_id = request.POST.get('category')
        subcategory.category = get_object_or_404(Category, pk=category_id)
        subcategory.save()
        messages.success(request, 'Subcategory updated successfully.')
        return redirect('manage_directories')
    categories = Category.objects.all()
    return render(request, 'cashflow/subcategory_form.html', {'subcategory': subcategory, 'categories': categories})

def subcategory_delete(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    if request.method == 'POST':
        subcategory.delete()
        messages.success(request, 'Subcategory deleted successfully.')
        return redirect('manage_directories')
    return render(request, 'cashflow/subcategory_confirm_delete.html', {'subcategory': subcategory})