from django.contrib import admin
from .models import Status, Type, Category, SubCategory, CashFlow


# Настройка отображения связанных подкатегорий в категориях
class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]
    list_display = ('name', 'type')
    list_filter = ('type',)


class CashFlowAdmin(admin.ModelAdmin):
    list_display = ('created_date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment')
    list_filter = ('created_date', 'status', 'type', 'category', 'subcategory')
    search_fields = ('comment',)


# Регистрация моделей в админке
admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory)
admin.site.register(CashFlow, CashFlowAdmin)
from django.contrib import admin

# Register your models here.
