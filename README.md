# Primer-Token

Quick task implementation


## Requirements
Python 3.7+ is required to run the application (using dataclasses and other nice-to-have python scaffolding)


## Installation
- To install, clone the repository locally: `git clone https://github.com/an-dev/primer-tokenizer`
- Create virtualenv: `python3.8 -m venv .venv`
- Activate virtualenv: `source .venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Migrate data/setup db `python manage.py migrate`


## Testing
Test via django built in command: `python manage.py test`

## Usage

**Note**: If you use `primer-token.herokuapp.com` as a host, beware that the heroku puts the server to sleep after 
30 minutes of inactivity, and your first call might timeout as the workers are being turned on.

The project was developed with Stripe, use any of the of their sandbox cards https://stripe.com/docs/testing#cards

### Tokenize credit card
Request
```
curl --request POST \
  --url http://localhost:8000/api/tokenize/ \
  --header 'Content-Type: application/json' \
  --data '{
        "number": "4242424242424242",
        "expiry_month": 10,
        "expiry_year": 2021
    }'
```

Successful Response
```
{
    "token": "tok_xxxxxx"
}

```

### Execute sale with token (obtained from API call above)
Request
```
curl --request POST \
  --url https://localhost:8000/api/sale/ \
  --header 'Content-Type: application/json' \
  --data '{
        "token": "tok_xxxxxx",
        "amount": 45000,
        "description": "Just your average description for a charge",
        "currency": "usd"
    }'
```

Successful Response
```
{
    "receipt_url": "https://pay.stripe.com/receipts/acct_xxxxx/ch_yyyyyyy/rcpt_zzzzz", # You can view the transaction/receipt here btw
    "transaction_id": "txn_xxxxx"
}
```

## Notes, Technical decisions et all

#### Choice of processor/connector
The project is heavily influenced by Stripe, as it was used as main/default choice as a connector, but it opens to possibility of implementing other connectors.

#### Data storage 
The project doesn't store any Customer/Card information, as it wasn't one of the explicit features requested by the task but this would be easily implementable.

`customer 1 -> n card`

`card 1 -> n tokens (single use)`

In the above scenario a "returning" user/card details would no create a new card but return:
- a non used token related to the card details inserted
- a new token

#### Enpoint Authorization/Authentication
If this was a publicly exposed API some sort of Authorization would be needed for a potential developer (along with other safeguards like rate limiting etc...)

#### Testing and logging
A minimalistic approach to testing was taken, using cassettes to speed up tests that may require external API calls to speed up test cases.
Potentially more comprehensive tests would be written (on the connectors for example).

As for logging and exception handling, common or expected errors are catched while leaving unexpected events bubble up (in a production environment we'd be notified about these with a `Sentry`-like system)


## References
Web pages used/consulted while building the script

https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset

https://www.django-rest-framework.org/api-guide/testing/#testing

https://stackoverflow.com/questions/31685688/is-allowed-hosts-needed-on-heroku
