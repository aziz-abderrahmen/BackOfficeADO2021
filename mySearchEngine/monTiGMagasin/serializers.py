from rest_framework.serializers import ModelSerializer
from monTiGMagasin.models import InfoProduct
from monTiGMagasin.models import Transaction

class InfoProductSerializer(ModelSerializer):
    class Meta:
        model = InfoProduct
        fields = ('id', 'tig_id', 'name', 'category', 'price', 'unit', 'availability', 'sale',
                  'discount', 'comments', 'owner', 'quantityInStock', 'nombre_produit_vendu', 'sell_price')

class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'created', 'price', 'quantity', 'tig_id', 'type')