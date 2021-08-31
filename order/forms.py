from django import forms

from order.models import Order, OrderItem
from products.models import Product


class OrderForms(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(OrderForms, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not field_name == 'status':
                field.widget.attrs['class'] = 'form-control py-4'
            else:
                field.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    price = forms.DecimalField(max_digits=8, decimal_places=2, label='Цена', required=False)

    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['product'].queryset = Product.objects.all().select_related()
