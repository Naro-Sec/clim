import authomatic
from authomatic.providers import oauth2

CONFIG = {
    'amazon': {
        'class_': oauth2.Amazon,
        'consumer_key': 'amzn1.application-oa2-client.9d9e5261e2454528a8f18606cd32e996',
        'consumer_secret': '7b90d10ea1b78575df5f698bd157566b2145d8084dee458a43b92400720f3f84',
        'id': authomatic.provider_id(),
        'scope': oauth2.Amazon.user_info_scope,
    },
    'google': {
     'class_': oauth2.Google,
     'consumer_key': '89289253880-7cpskjsbnura71srijad1nfsvkkvt1ik.apps.googleusercontent.com',
     'consumer_secret': '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',
     'id': authomatic.provider_id(),
     'scope': oauth2.Google.user_info_scope + [
     'https://www.googleapis.com/auth/calendar',
     'https://mail.google.com/mail/feed/atom',
     'https://www.googleapis.com/auth/drive',
     'https://gdata.youtube.com'],
     '_apis': {
         'List your calendars': ('GET',
        'https://www.googleapis.com/calendar/v3/users/me/calendarList'),
         'List your YouTube playlists': ('GET',
        'https://gdata.youtube.com/feeds/api/users/default/playlists?alt=json'),
     },
    },
}