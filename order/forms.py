from django import forms

from order.models import Order, OrderItem


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
    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
