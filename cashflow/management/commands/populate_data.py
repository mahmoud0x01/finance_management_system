from django.core.management.base import BaseCommand
from cashflow.models import Status, Type, Category, SubCategory, CashFlow
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populates the database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data (optional)
        CashFlow.objects.all().delete()
        SubCategory.objects.all().delete()
        Category.objects.all().delete()
        Type.objects.all().delete()
        Status.objects.all().delete()

        # Add Statuses
        statuses = ["Бизнес", "Личное", "Налог"]
        for name in statuses:
            Status.objects.get_or_create(name=name)

        # Add Types
        types = ["Пополнение", "Списание"]
        type_objs = {}
        for name in types:
            type_objs[name], _ = Type.objects.get_or_create(name=name)

        # Add Categories
        categories = {
            "Пополнение": ["Доход"],
            "Списание": ["Маркетинг", "Инфраструктура"]
        }
        category_objs = {}
        for type_name, cat_list in categories.items():
            for cat_name in cat_list:
                category_objs[cat_name], _ = Category.objects.get_or_create(
                    name=cat_name, type=type_objs[type_name]
                )

        # Add SubCategories
        subcategories = {
            "Маркетинг": ["Farpost", "Avito"],
            "Инфраструктура": ["VPS", "Proxy"],
            "Доход": ["Зарплата"]  # Added a subcategory for Доход
        }
        subcategory_objs = {}
        for cat_name, sub_list in subcategories.items():
            for sub_name in sub_list:
                subcategory_objs[sub_name], _ = SubCategory.objects.get_or_create(
                    name=sub_name, category=category_objs[cat_name]
                )

        # Add CashFlow Records
        test_data = [
            {
                "created_date": timezone.now().date(),
                "status": Status.objects.get(name="Бизнес"),
                "type": type_objs["Списание"],
                "category": category_objs["Маркетинг"],
                "subcategory": subcategory_objs["Avito"],
                "amount": 1000.00,
                "comment": "Реклама на Avito"
            },
            {
                "created_date": timezone.now().date(),
                "status": Status.objects.get(name="Личное"),
                "type": type_objs["Пополнение"],
                "category": category_objs["Доход"],
                "subcategory": subcategory_objs["Зарплата"],  # Now using a valid subcategory
                "amount": 5000.00,
                "comment": "Зарплата"
            },
            {
                "created_date": timezone.now().date(),
                "status": Status.objects.get(name="Налог"),
                "type": type_objs["Списание"],
                "category": category_objs["Инфраструктура"],
                "subcategory": subcategory_objs["VPS"],
                "amount": 2000.00,
                "comment": "Налог на сервер"
            },
        ]

        for data in test_data:
            CashFlow.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data!'))