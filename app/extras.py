from django.conf import settings
import random
import string
from datetime import date
import datetime
import braintree
from app.models import OrderTow
from django.conf import settings
def generate_order_id():
    date_str = date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return date_str + rand_str

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=braintree.Environment.Sandbox,
        merchant_id='7gtb5f7ts5ycqhf5',
        public_key='jshhnqfshcr9bpvm',
        private_key='7552ae54f058d94faa5ae969d19e1e12'
    )
)

def generate_client_token():
    return gateway.client_token.generate()

def transact(options):
    return gateway.transaction.sale(options)

def find_transaction(id):
    return gateway.transaction.find(id)