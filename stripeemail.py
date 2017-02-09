import json
import falcon
import os

import stripe

from emailsender import send_mail


class StripeEmailResource:
    def on_post(self, req, resp):
        try:
            event_json = json.load(req.stream, 'utf-8')
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect.')

        stripe.api_key = os.environ["STRIPE_KEY"]
        if event_json["type"] in ("charge.succeeded", "charge.failed", "charge.refunded", "charge.captured",
                                  "charge.updated", "charge.dispute.created", "charge.dispute.updated",
                                  "charge.dispute.closed", "customer.created", "customer.subscription.created",
                                  "customer.subscription.updated", "invoice.created", "invoice.updated",
                                  "invoice.payment_succeeded", "invoice.payment_failed", "transfer.failed"):
            try:
                id = event_json["id"]
                event = stripe.Event.retrieve(id)
                send_mail(("billing@example.com",), event_json["type"], str(event))
            except (stripe.error.InvalidRequestError, stripe.error.AuthenticationError,
                    stripe.error.APIConnectionError, stripe.error.StripeError) as err:
                send_mail(("billing@example.com",), "Stripe Webhook Error", str(err.json_body['error']))

        resp.status = falcon.HTTP_200  # This is the default status


# falcon.API instances are callable WSGI apps
app = falcon.API()

stripeemail = StripeEmailResource()

app.add_route('/webhook/receive', stripeemail)

