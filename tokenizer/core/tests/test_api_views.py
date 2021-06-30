import vcr
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

FIXTURE_PATH = 'tokenizer/core/tests/cassettes'


# Tokenize Endpoint
class TokenizeTests(APITestCase):

    def setUp(self):
        self.url = reverse('core.tokenize')

    def test_create_token_fails_no_data(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {"number": ["This field is required."], "expiry_month": ["This field is required."],
                          "expiry_year": ["This field is required."]})

    def test_create_token_fails_missing_key(self):
        response = self.client.post(self.url, {
            "expiry_month": 10,
            "expiry_year": 2021
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {"number": ["This field is required."]})

    @vcr.use_cassette(f'{FIXTURE_PATH}/test_create_token_fails_card_error.yaml', record_mode='new_episodes')
    def test_create_token_fails_card_error(self):
        response = self.client.post(self.url, {
            "number": "4242424242424241",
            "expiry_month": 10,
            "expiry_year": 2021
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"error": "Request req_boKNpt0pRDjD48: Your card number is incorrect."})

    @vcr.use_cassette(f'{FIXTURE_PATH}/test_create_token_success.yaml', record_mode='new_episodes')
    def test_create_token_success(self):
        today = timezone.now()
        response = self.client.post(self.url, {
            "number": "4242424242424242",
            "expiry_month": 10,
            "expiry_year": today.date().year + 1
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'token': 'tok_1J8Aqp2eZvKYlo2C9EjfKC3y'})

    @vcr.use_cassette(f'{FIXTURE_PATH}/test_create_token_success_cvc.yaml', record_mode='new_episodes')
    def test_create_token_success_cvc(self):
        today = timezone.now()
        response = self.client.post(self.url, {
            "number": "4242424242424242",
            "expiry_month": 10,
            "expiry_year": today.date().year + 1,
            "cvc": "343"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'token': 'tok_1J8B2W2eZvKYlo2C1UNsoBxb'})


# Sale Endpoint
class SaleTests(APITestCase):
    def setUp(self):
        self.url = reverse('core.sale')

    def test_sale_fails_no_data(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {"token": ["This field is required."], "currency": ["This field is required."],
                          "description": ["This field is required."], "amount": ["This field is required."]})

    def test_sale_fails_no_token(self):
        response = self.client.post(self.url, {
            "amount": 24500,
            "description": "Just your average description for a charge",
            "currency": "usd"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
            "token": [
                "This field is required."
            ]
        })

    @vcr.use_cassette(f'{FIXTURE_PATH}/test_sale_success.yaml', record_mode='new_episodes')
    def test_sale_success(self):
        response = self.client.post(self.url, {
            "token": "tok_1J8C9w2eZvKYlo2CMhHS7Ug9",
            "amount": 24500,
            "description": "Just your average description for a charge",
            "currency": "usd"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "receipt_url": "https://pay.stripe.com/receipts/acct_1032D82eZvKYlo2C/ch_1J8CA92eZvKYlo2CLpvXjCSY/rcpt_JljdjRSbcsSxFaEKCNeBm7ijYhqa9Nj",
            "transaction_id": "txn_1J8CA92eZvKYlo2CxSX4hpn8"
        })

    @vcr.use_cassette(f'{FIXTURE_PATH}/test_sale_fails_token_already_used.yaml', record_mode='new_episodes')
    def test_sale_fails_token_already_used(self):
        response = self.client.post(self.url, {
            "token": "tok_1J8C9w2eZvKYlo2CMhHS7Ug9",
            "amount": 14500,
            "description": "Just your average description for a charge (cheeky version)",
            "currency": "eur"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Request req_66yL6CXfxKj2wj: You cannot use a Stripe token more than once: tok_1J8C9w2eZvKYlo2CMhHS7Ug9.'})
