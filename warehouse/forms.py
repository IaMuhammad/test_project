from decimal import Decimal

from django import forms

from warehouse.models import Manufacture, Product, Warehouse


class ManufactureForm(forms.ModelForm):
    class Meta:
        model = Manufacture
        fields = '__all__'

    def clean_quantity_save(self, quantity, product_id):
        product = Product.objects.filter(id=product_id).first()
        product_material_list = product.productmaterial_set.all()
        for product_material in product_material_list:
            material = product_material.material
            warehouse_material = Warehouse.objects.filter(
                material=material, remainder__gte=product_material.quantity * quantity
            ).first()
            if not warehouse_material:
                raise forms.ValidationError(f'We dont have this amount of material ({material.name})')

    def clean_quantity_change(self, quantity, product_id):
        quantity = quantity - self.instance.quantity
        product = Product.objects.filter(id=product_id).first()
        for warehouse_material in self.instance.warehouse.all():
            material = warehouse_material.material
            product_material = product.productmaterial_set.filter(material=material).first()
            if warehouse_material.remainder < product_material.quantity * quantity:
                raise forms.ValidationError(f'We dont have this amount of material ({material.name})')

    def clean_quantity(self):
        quantity = Decimal(self.cleaned_data.get('quantity', 0))
        product_id = self.data.get('product')
        if self.instance.pk:
            self.clean_quantity_change(quantity, product_id)
        else:
            self.clean_quantity_save(quantity, product_id)
        return quantity

    def save(self, commit=True):
        form = super().save(commit)
        return form
