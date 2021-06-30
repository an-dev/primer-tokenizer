from dataclasses import dataclass

from tokenizer.core.connectors.stripe_connector import StripeConnector


@dataclass
class TokenizeService:
    number: str
    expiry_month: int
    expiry_year: int
    cvc: str = ''

    def run(self, connector=StripeConnector):
        return connector().tokenize(number=self.number, expiry_month=self.expiry_month, expiry_year=self.expiry_year,
                                    cvc=self.cvc)


@dataclass
class SaleService:
    amount: int
    currency: str
    description: str
    token: str

    def run(self, connector=StripeConnector):
        return connector().charge(amount=self.amount, currency=self.currency, description=self.description,
                                  token=self.token)
