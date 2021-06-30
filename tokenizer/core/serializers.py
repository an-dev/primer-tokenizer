from rest_framework import serializers

from tokenizer.core.models import Card


class CardSerializer(serializers.ModelSerializer):
    cvc = serializers.CharField(min_length=3, max_length=3, required=False)

    class Meta:
        model = Card
        fields = ['number', 'expiry_month', 'expiry_year', 'cvc']


class SaleSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=100)  # Stripe handles currency in cents 100 <currency> = 1 <currency>
    currency = serializers.CharField(min_length=3, max_length=3)
    description = serializers.CharField(min_length=5, max_length=512)
    token = serializers.CharField(min_length=10)  # Purely fictional, not sure how long non-stripe tokens are

    class Meta:
        fields = ['amount', 'currency', 'description', 'token']

    def to_internal_value(self, data):
        if data.get('currency'):
            validated_data = data.copy()  # a copy() on a Querydict in this instance returns a deep-copied objec
            currency = data['currency'].lower()
            validated_data.__setitem__('currency', currency)
            return super(SaleSerializer, self).to_internal_value(validated_data)
        return super(SaleSerializer, self).to_internal_value(data)
