from django.contrib import admin

from warehouse.models import ProductMaterial


class MaterialTabularInline(admin.TabularInline):
    model = ProductMaterial
