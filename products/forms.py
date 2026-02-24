from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'discount_price', 'stock', 'image', 'is_available', 'is_on_sale', 'sale_badge_text']
        labels = {
            'name': 'Product Name',
            'discount_price': 'Discount Price (Optional)',
        }
