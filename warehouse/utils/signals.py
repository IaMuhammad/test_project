from decimal import Decimal

from django.db import transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver

from warehouse.models import Manufacture, Warehouse


@transaction.atomic
@receiver(pre_save, sender=Manufacture)
def pre_save_defective_product(sender, instance: Manufacture, *args, **kwargs):
    # last_data = Manufacture.objects.filter(id=instance.pk).first()
    # if last_data:
    #     quantity = instance.quantity - (last_data.quantity if last_data else Decimal(0))
    # else:
    #     quantity = instance.quantity
    # product_material_list = instance.product.productmaterial_set.all()
    # for product_material in product_material_list:
    #     material = product_material.material
    #     warehouse_material = Warehouse.objects.filter(
    #         material=material, remainder__gte=product_material.quantity * quantity
    #     ).first()
    #     if warehouse_material:
    #         # instance.warehouse.add(warehouse_material)
    #         warehouse_material.remainder -= product_material.quantity * quantity
    #         warehouse_material.save()
    pass
