from unittest import TestCase

from tokenizer.core.serializers import SaleSerializer


class SaleSerializerTests(TestCase):

    def setUp(self):
        self.serializer = SaleSerializer

    def test_sale_serialzer_currency(self):
        currency = "USD"
        data = {
            "token": "just-a-token",
            "amount": 11500,
            "description": "foo-bar",
            "currency": currency
        }
        serializer = self.serializer(data=data)
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(serializer.validated_data['currency'], currency.lower())