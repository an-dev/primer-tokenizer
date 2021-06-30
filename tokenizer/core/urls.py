from django.urls import path

from tokenizer.core.views import TokenizeApiView, SaleApiView

urlpatterns = [
    path('tokenize/', TokenizeApiView.as_view(), name='core.tokenize'),
    path('sale/', SaleApiView.as_view(), name='core.sale'),
]
