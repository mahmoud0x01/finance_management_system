from django import forms
from .models import CashFlow, Category, SubCategory, Type, Status

class CashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = ['created_date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'created_date': forms.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].required = True
        self.fields['category'].required = True
        self.fields['subcategory'].required = True
        self.fields['amount'].required = True

        self.fields['category'].queryset = Category.objects.all()
        self.fields['subcategory'].queryset = SubCategory.objects.none()

        if 'type' in self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.type:
            self.fields['category'].queryset = Category.objects.filter(type=self.instance.type)

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.category:
            self.fields['subcategory'].queryset = SubCategory.objects.filter(category=self.instance.category)

    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data.get('type')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        amount = cleaned_data.get('amount')

        if not type:
            self.add_error('type', 'Type is required.')
        if not category:
            self.add_error('category', 'Category is required.')
        if not subcategory:
            self.add_error('subcategory', 'Subcategory is required.')
        if not amount:
            self.add_error('amount', 'Amount is required.')
        elif amount <= 0:
            self.add_error('amount', 'Amount must be greater than zero.')

        if category and subcategory and subcategory.category != category:
            self.add_error('subcategory', 'Subcategory does not belong to the selected category.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('created_date'):
            instance.created_date = self.cleaned_data['created_date']
        if commit:
            instance.save()
        return instance

class CashFlowFilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=False)
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    subcategory = forms.ModelChoiceField(queryset=SubCategory.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].empty_label = "All Statuses"
        self.fields['type'].empty_label = "All Types"
        self.fields['category'].empty_label = "All Categories"
        self.fields['subcategory'].empty_label = "All Subcategories"