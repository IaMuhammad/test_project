from rest_framework import serializers

from warehouse.models import Manufacture


class ManufactureSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(max_length=255, source='product.name')
    product_qty = serializers.DecimalField(max_digits=20, decimal_places=2, source='quantity')
    product_materials = serializers.SerializerMethodField()

    class Meta:
        model = Manufacture
        fields = ('id', 'product_name', 'product_qty', 'product_materials')

    def get_product_materials(self, obj: Manufacture):
        _list = []
        for item in obj.warehouse.all():
            product_material = obj.product.productmaterial_set.filter(material=item.material).first()
            _list.append({
                'warehouse_id': item.id,
                'material_name': item.material.name,
                'qty': product_material.quantity * obj.quantity,
                'price': item.price
            })
        return _list
