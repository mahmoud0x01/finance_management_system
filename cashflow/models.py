from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Справочник: Статусы
class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Справочник: Типы (Пополнение/Списание)
class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Справочник: Категории (привязаны к типам)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return self.name

# Справочник: Подкатегории (привязаны к категориям)
class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    class Meta:
        unique_together = ('name', 'category')

# Основная модель: Запись о движении денежных средств
class CashFlow(models.Model):
    created_date = models.DateField(default=timezone.now)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)  # Made optional
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True, null=True)

    def clean(self):
        # Валидация: Категория должна соответствовать типу
        if self.category.type != self.type:
            raise ValidationError("Категория не соответствует выбранному типу.")
        # Валидация: Если подкатегория указана, она должна соответствовать категории
        if self.subcategory and self.subcategory.category != self.category:
            raise ValidationError("Подкатегория не соответствует выбранной категории.")

    def __str__(self):
        return f"{self.created_date} - {self.amount} руб. ({self.type.name})"