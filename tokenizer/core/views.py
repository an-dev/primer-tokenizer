from rest_framework import views, status
from rest_framework.response import Response

from tokenizer.core.serializers import CardSerializer, SaleSerializer
from tokenizer.core.services import TokenizeService, SaleService


class TokenizeApiView(views.APIView):
    def post(self, request):
        serializer = CardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        result = TokenizeService(**data).run()
        if result.get('error'):
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        token = result['success']
        return Response({'token': token}, status=status.HTTP_200_OK)


class SaleApiView(views.APIView):
    def post(self, request):
        serializer = SaleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        result = SaleService(**data).run()
        if result.get('error'):
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response({'receipt_url': result['success']['receipt_url'], 'transaction_id': result['success']['transaction_id']}, status=status.HTTP_200_OK)
