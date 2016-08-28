import json
from flask import Flask, jsonify, make_response
from webargs import fields
from webargs.flaskparser import use_args
from instance_pricing.utils import func
from instance_pricing.custom_exceptions import InvalidUsage

app = Flask(__name__)

#----------------------------------------
# logging
#----------------------------------------
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


#----------------------------------------
# controllers
#----------------------------------------

import os.path

d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pricing_file = os.path.join(d, 'pricing-on-demand-instances.json')
try:
    with open(pricing_file) as file:
        data = json.loads(file.read())['config']['regions']
except IOError:
    raise Exception("pricing-on-demand-instances.json does not exist.")
# Extract instance types & prices per region
pricing_per_region = func(data)

# Required params
pricing_args = {
    'region': fields.Str(required=True),
    'instance_type': fields.Str(required=True)
}


@app.before_request
def log_entry():
    logger.debug("Handling request")


@app.teardown_request
def log_exit(exc):
    logger.debug("Finished handling request")


@app.route('/', methods=["GET"])
def RootAPI():
    return 'OK'


@app.route('/v1/pricing', methods=["POST", "GET"])
@use_args(pricing_args)
def PricingAPI(args):
    if not args['region'] in pricing_per_region:
        msg = 'Region %s does not exist' % args['region']
        logger.error(msg)
        raise InvalidUsage(msg, status_code=404)
    if not args['instance_type'] in pricing_per_region[args['region']]:
        msg = 'InstanceType %s does not exist in region %s' % (
            args['instance_type'], args['region'])
        logger.error(msg)
        raise InvalidUsage(msg, status_code=404)

    price = pricing_per_region[args['region']][args['instance_type']]
    logger.debug("Returned price: %s" % price)
    return price


#----------------------------------------
# error handlers
#----------------------------------------

# Custom error handler
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(400)
def bad_request(error):
    logger.error('Bad request')
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    logger.error('Not found')
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(405)
def not_allowed(error):
    logger.error('Method not allowed')
    return make_response(jsonify({'error': 'Method not allowed'}), 405)


# Return validation errors as JSON
@app.errorhandler(422)
def handle_validation_error(error):
    exc = error.data['exc']
    logger.error(exc)
    return make_response(jsonify({'errors': exc.messages}), 422)
