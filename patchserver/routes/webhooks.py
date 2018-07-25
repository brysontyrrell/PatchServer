import functools
import time

from flask import current_app, g, url_for
import requests

from patchserver.models import WebhookUrls


def webhook_event(func):
    """A decorator that will send a webhook event notification to a all URLs
    saved in the Patch Server database.
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        response = func(*args, **kwargs)
        current_app.logger.debug('Webhook event invoked')

        for webhook_url in WebhookUrls.query.all():
            if webhook_url.enabled:
                current_app.logger.debug(
                    'Sending event to: {}'.format(webhook_url.url))
                event = {
                    "event": g.event_type,
                    "timestamp": int(time.time()),
                    "software_title": g.event['id'],
                    "version:": g.event['currentVersion'],
                    "url": url_for(
                        'jamf_pro.patch_by_name_id', name_id=g.event['id'])
                }
                if webhook_url.send_definition:
                    event['patch_definition'] = g.event

                try:
                    requests.post(
                        webhook_url.url,
                        json=event,
                        timeout=5,
                        verify=webhook_url.verify_ssl
                    )
                except requests.RequestException as err:
                    current_app.logger.exception('The webhook failed!')

            else:
                current_app.logger.info('The webhook is not enabled for: '
                                        '{}'.format(webhook_url.url))

        current_app.logger.debug('Webhook event complete')

        return response

    return wrapped
