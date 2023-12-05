import authomatic
from authomatic.providers import oauth2

CONFIG = {
    'amazon': {
        'class_': oauth2.Amazon,
        'consumer_key': '',
        'consumer_secret': '',
        'id': authomatic.provider_id(),
        'scope': oauth2.Amazon.user_info_scope,
    },
    'google': {
     'class_': oauth2.Google,
     'consumer_key': '',
     'consumer_secret': '',
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
