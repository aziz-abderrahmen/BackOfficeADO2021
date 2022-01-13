from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from monTiGMagasin.config import baseUrl
from monTiGMagasin.models import InfoProduct
from monTiGMagasin.serializers import InfoProductSerializer
from monTiGMagasin.models import ProduitPoissons
from monTiGMagasin.serializers import ProduitPoissonsSerializer
from monTiGMagasin.models import ProduitCrustaces
from monTiGMagasin.serializers import ProduitCrustacesSerializer
from monTiGMagasin.models import ProduitCoquillages
from monTiGMagasin.serializers import ProduitCoquillagesSerializer
from monTiGMagasin.serializers import TransactionSerializer
from monTiGMagasin.models import Transaction

# Create your views here.
class InfoProductList(APIView):
    def get(self, request, format=None):
        products = InfoProduct.objects.all()
        serializer = InfoProductSerializer(products, many=True)
        return Response(serializer.data)
        
class InfoProductDetail(APIView):
    def get_object(self, tig_id):
        try:
            return InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404
    def get(self, request, tig_id, format=None):
        product = self.get_object(tig_id=tig_id)
        serializer = InfoProductSerializer(product)
        return Response(serializer.data)
        
class ProductIncrementStock(APIView):
    def get_object(self, tig_id):
        try:
            return InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404

    def get(self, request, tig_id, number, format=None):
        productBefore = InfoProduct.objects.get(tig_id=tig_id)
        productBefore.quantityInStock = productBefore.quantityInStock + number
        productBefore.save()
        
        product = self.get_object(tig_id=tig_id)
        serializer = InfoProductSerializer(product)
        return Response(serializer.data)
        
class ProductDecrementStock(APIView):
    def get_object(self, tig_id):
        try:
            return InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404

    def get(self, request, tig_id, number, format=None):
        productBefore = InfoProduct.objects.get(tig_id=tig_id)
        if productBefore.quantityInStock - number >= 0 :
            productBefore.quantityInStock = productBefore.quantityInStock - number
            productBefore.save()
        
        product = self.get_object(tig_id=tig_id)
        serializer = InfoProductSerializer(product)
        return Response(serializer.data)


class ProductModifyDiscount(APIView):
    def get_object(self, tig_id):
        try:
            return InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404

    def get(self, request, tig_id, number, format=None):
        productBefore = InfoProduct.objects.get(tig_id=tig_id)
        if number == 0:
            productBefore.sale = False
            productBefore.discount = 0
        else :
            if number <= 100:
                if productBefore.sale == False:
                    productBefore.sale = True
                productBefore.discount = number
        productBefore.save()

        product = self.get_object(tig_id=tig_id)
        serializer = InfoProductSerializer(product)
        return Response(serializer.data)
class PoissonsproductList(APIView):
    def get_object(self, tig_id):
        try:
            return InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        res = []
        for prod in ProduitPoissons.objects.all():
            serializerPoisson = ProduitPoissonsSerializer(prod)
            product = self.get_object(tig_id=serializerPoisson.data['tigID'])
            serializer = InfoProductSerializer(product)
            res.append(serializer.data)
        return Response(res)

class CrustacesproductList(APIView):
    def get_object(self, tig_id):
        try:
            return InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        res = []
        for prod in ProduitCrustaces.objects.all():
            serializerCrustaces = ProduitCrustacesSerializer(prod)
            product = self.get_object(tig_id=serializerCrustaces.data['tigID'])
            serializer = InfoProductSerializer(product)
            res.append(serializer.data)
        return Response(res)


class CoquillagesproductList(APIView):
    def get_object(self, tig_id):
        try:
            return InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            return
            # raise Http404

    def get(self, request, format=None):
        res = []
        for prod in ProduitCoquillages.objects.all():
            serializerCoquillages = ProduitCoquillagesSerializer(prod)
            product = self.get_object(tig_id=serializerCoquillages.data['tigID'])
            serializer = InfoProductSerializer(product)
            res.append(serializer.data)
        return Response(res)

class ModifierPrixVente(APIView):
    def get_object(self, tig_id):
        try:
            return InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404

    def get(self, request, tig_id, price, format=None):
        productBefore = InfoProduct.objects.get(tig_id=tig_id)
        productBefore.sell_price = price
        productBefore.save()

        product = self.get_object(tig_id=tig_id)
        serializer = InfoProductSerializer(product)
        return Response(serializer.data)


class addTransaction(APIView):
    def get(self, request, format=None):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            product = InfoProduct.objects.get(tig_id=serializer.data['tig_id'])
            if serializer.data['type'] == "Sale":
                product.nombre_produit_vendu = product.nombre_produit_vendu + serializer.data['quantity']
                product.quantityInStock = product.quantityInStock - int(serializer.data['quantity'])
            elif serializer.data['type'] == "Unsold":
                product.quantityInStock = product.quantityInStock - int(serializer.data['quantity'])
            elif serializer.data['type'] == "Purchase":
                product.quantityInStock = product.quantityInStock + int(serializer.data['quantity'])
            product.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class getTransactionCategory(APIView):
    def get_object(self, tig_id):
        try:
            return InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404
    
    def get(self, request, idCategory, format=None):
        transactions = Transaction.objects.all()
        serializerTransaction = TransactionSerializer(transactions, many=True)
        res = []
        for transac in serializerTransaction.data:
            product = self.get_object(tig_id=transac['tig_id'])
            serializerProduct = InfoProductSerializer(product)
            if (serializerProduct.data['category'] == idCategory):
                res.append(transac)
        return Response(res)