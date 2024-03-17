from decimal import Decimal

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import transaction

from warehouse.forms import ManufactureForm
from warehouse.utils.inline import MaterialTabularInline
from warehouse.models import Product, Material, Warehouse, UnitSize, Manufacture


# Register your models here.
@admin.register(UnitSize)
class UnitSizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    inlines = [MaterialTabularInline]


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'material', 'remainder', 'price')


@admin.register(Manufacture)
class ManufactureAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity')
    readonly_fields = ('warehouse',)
    form = ManufactureForm

    def save_model(self, request, obj: Manufacture, form, change):
        last_data = Manufacture.objects.filter(id=obj.pk).first()
        super().save_model(request, obj, form, change)
        if change:
            quantity = obj.quantity - (last_data.quantity if last_data else Decimal(0))
            product = Product.objects.filter(id=form.data.get('product')).first()
            for warehouse_material in obj.warehouse.all():
                material = warehouse_material.material
                product_material = product.productmaterial_set.filter(material=material).first()
                warehouse_material.remainder -= product_material.quantity * quantity
                warehouse_material.save()
        else:
            quantity = obj.quantity
            product = Product.objects.filter(id=form.data.get('product')).first()
            product_material_list = product.productmaterial_set.all()
            for product_material in product_material_list:
                material = product_material.material
                warehouse_material = Warehouse.objects.filter(
                    material=material, remainder__gte=product_material.quantity * quantity
                ).first()
                if warehouse_material:
                    obj.warehouse.add(warehouse_material)
                    warehouse_material.remainder -= product_material.quantity * quantity
                    warehouse_material.save()
