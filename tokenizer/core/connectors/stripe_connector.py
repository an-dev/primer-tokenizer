import logging

import stripe
from dataclasses import dataclass
from django.conf import settings
from tokenizer.core.connectors import Connector

stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)


@dataclass
class StripeConnector(Connector):

    def tokenize(self, number: str, expiry_month: int, expiry_year: int, cvc: str = ''):
        card_details = {
            "number": number,
            "exp_month": expiry_month,
            "exp_year": expiry_year,
        }
        if cvc:
            card_details.update({'cvc': cvc})

        try:
            stripe_response = stripe.Token.create(
                card=card_details
            )
            result = {'success': stripe_response['id']}
        except (stripe.error.StripeError, IndexError) as e:
            logger.error('Failed attempt to tokenize', self.__class__.__name__)
            result = {'error': str(e)}
        return result

    def charge(self, amount: int, currency: str, description: str, token: str):
        try:
            stripe_response = stripe.Charge.create(
                amount=amount, currency=currency, description=description, source=token
            )
            result = {'success': {'receipt_url': stripe_response['receipt_url'],
                                  'transaction_id': stripe_response['balance_transaction']}}
        except (stripe.error.StripeError, IndexError) as e:
            logger.error('Failed attempt to charge', self.__class__.__name__)
            result = {'error': str(e)}
        return result


