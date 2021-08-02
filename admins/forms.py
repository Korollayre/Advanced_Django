from django import forms
from users.forms import UserRegistrationForm, UserProfileForm
from users.models import User
from products.models import Product, ProductCategory


class UserAdminRegistrationForm(UserRegistrationForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'image', 'first_name', 'last_name', 'password1', 'password2')


class UserAdminProfileForm(UserProfileForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4'}))


class ProductCategoryAdminForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4'}))
    description = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4'}))

    class Meta:
        model = ProductCategory
        fields = ('name', 'description')
