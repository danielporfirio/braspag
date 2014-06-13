# -*- encoding: utf-8 -*-

import sys
import uuid
import logging
from tornado import ioloop
from datetime import timedelta

from pprint import pformat
from braspag.core import BraspagRequest
from braspag.consts import PAYMENT_METHODS

# log setup
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

if len(sys.argv) > 1:
    MERCHANT_ID = sys.argv[1]
else:
    MERCHANT_ID = u'F9B44052-4AE0-E311-9406-0026B939D54B'

# Create request object
request = BraspagRequest(merchant_id=MERCHANT_ID, homologation=True)

def capture_callback(response):
    logging.info(pformat(response.__dict__))
    logging.info('captured! transaction_id: %s' % response.braspag_order_id)

    ioloop.IOLoop.instance().stop()

def authorize_callback(response):
    logging.info(pformat(response.__dict__))
    logging.info('transaction_id: %s' % response.braspag_order_id)

    # capture the transaction
    for transaction in response.transactions:
        braspag_transaction_id = transaction['braspag_transaction_id']
        logging.info('firing request to capture: %s' % braspag_transaction_id)
        request.capture(capture_callback, transaction_id=braspag_transaction_id)

# Authorize
logging.info('firing request')
request.authorize(
    authorize_callback,
    request_id=u'782a56e2-2dae-11e2-b3ee-080027d29772',
    order_id=uuid.uuid4(),
    customer_id=u'12345678900',
    customer_name=u'José da Silva',
    customer_email='jose123@dasilva.com.br',
    transactions=[
        {
        'amount': 10000,
        'card_holder': 'Jose da Silva',
        'card_number': '0000000000000001',
        'card_security_code': '123',
        'card_exp_date': '05/2018',
        'save_card': True,
        'payment_method': PAYMENT_METHODS['Simulated']['BRL'],
    },{
        'amount': 20000,
        'card_holder': 'Paulo da Silva',
        'card_number': '9000000000000001',
        'card_security_code': '123',
        'card_exp_date': '01/2018',
        'save_card': True,
        'payment_method': PAYMENT_METHODS['Simulated']['BRL'],
    }],
)
logging.info('fired')

# Void
#response3 = request.void(transaction_id=response.transaction_id)
#logging.info(pformat(response3.__dict__))

def dot():
    logging.debug(u'iteration')
    ioloop.IOLoop.instance().add_timeout(timedelta(seconds=1), dot)

ioloop.IOLoop.instance().add_timeout(timedelta(seconds=1), dot)
ioloop.IOLoop.instance().start()
