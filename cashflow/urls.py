from django.urls import path
from . import views

urlpatterns = [
    path('', views.cashflow_list, name='cashflow_list'),  # Главная страница со списком записей
    path('create/', views.cashflow_create, name='cashflow_create'),  # Создание записи
    path('edit/<int:pk>/', views.cashflow_edit, name='cashflow_edit'),  # Редактирование записи
    path('delete/<int:pk>/', views.cashflow_delete, name='cashflow_delete'),  # Удаление записи
    path('directories/', views.manage_directories, name='manage_directories'),  # Управление справочниками
    path('status/create/', views.status_create, name='status_create'),
    path('status/edit/<int:pk>/', views.status_edit, name='status_edit'),
    path('status/delete/<int:pk>/', views.status_delete, name='status_delete'),
    path('type/create/', views.type_create, name='type_create'),
    path('type/edit/<int:pk>/', views.type_edit, name='type_edit'),
    path('type/delete/<int:pk>/', views.type_delete, name='type_delete'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('category/delete/<int:pk>/', views.category_delete, name='category_delete'),
    path('subcategory/create/', views.subcategory_create, name='subcategory_create'),
    path('subcategory/edit/<int:pk>/', views.subcategory_edit, name='subcategory_edit'),
    path('subcategory/delete/<int:pk>/', views.subcategory_delete, name='subcategory_delete'),
    path('get_categories/', views.get_categories, name='get_categories'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
    path('get_all_categories/', views.get_all_categories, name='get_all_categories'),
    path('get_all_subcategories/', views.get_all_subcategories, name='get_all_subcategories'),
]