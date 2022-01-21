from django.urls import path
from monTiGMagasin import views
from django.urls import path, register_converter
from . import converts

register_converter(converts.FloatUrlParameterConverter, 'float')


urlpatterns = [
    path('infoproducts/', views.InfoProductList.as_view()),
    path('infoproduct/<int:tig_id>/', views.InfoProductDetail.as_view()),
    path('incrementStock/<int:tig_id>/<int:number>/', views.ProductIncrementStock.as_view()),
    path('decrementStock/<int:tig_id>/<int:number>/', views.ProductDecrementStock.as_view()),
    path('modifyDiscount/<int:tig_id>/<int:number>/', views.ProductModifyDiscount.as_view()),
    path('putonsale/<int:tig_id>/<float:newprice>/', views.ProductPutOnSale.as_view()),
    path('removesale/<int:tig_id>/', views.ProductRemoveSale.as_view()),
    path('productsByCategory/<int:category>/', views.ProductsByCategory.as_view()),
    path('ModifySellPrice/<int:tig_id>/<int:price>/', views.ModifierPrixVente.as_view()),
    path('transactions/', views.addTransaction.as_view()),
    path('transactions/<int:idCategory>/', views.getTransactionCategory.as_view()),
    path('infoproducts/<int:category>/', views.getProductsByCategory.as_view()),
]

