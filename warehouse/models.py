from decimal import Decimal

from django.db import models


# Create your models here.
class UnitSize(models.Model):  # this is name of unit sizes (kg, dona, m)
    name = models.CharField(max_length=255, unique=True)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Product(models.Model):  # this is product model
    name = models.CharField(max_length=255)  # name of product
    code = models.CharField(max_length=255, unique=True)  # code of product
    unit_size = models.ForeignKey('warehouse.UnitSize', on_delete=models.PROTECT)  # relationship with unit size

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Material(models.Model):  # material model
    name = models.CharField(max_length=255)  # name of material
    unit_size = models.ForeignKey('warehouse.UnitSize', on_delete=models.PROTECT)  # relationship with unit size

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class ProductMaterial(models.Model):  # extra model for connect to 2 db as M2M
    product = models.ForeignKey('warehouse.Product', on_delete=models.CASCADE)
    material = models.ForeignKey('warehouse.Material', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0))  # quantity of material


class Warehouse(models.Model):
    material = models.ForeignKey('warehouse.Material', on_delete=models.CASCADE)  # relationship with material
    remainder = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0))  # quantity of this material
    price = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0))  # price of this material

    def __str__(self):
        return f'{self.material} - {self.remainder} {self.material.unit_size.name} - {self.price}'


class Manufacture(models.Model):  # manufacture model for manufacture products
    product = models.ForeignKey('warehouse.Product', on_delete=models.CASCADE)  # relationship with material
    quantity = models.DecimalField(max_digits=20, decimal_places=2,
                                   default=Decimal(0))  # quantity of manfuactured product
    warehouse = models.ManyToManyField('warehouse.Warehouse')
