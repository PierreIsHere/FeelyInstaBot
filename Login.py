from instagram_private_api import Client, ClientCompatPatch
import json
import codecs
import datetime
import os.path

user_name = ''
password = ''
api = 0
settings_file_path = "login_cache.json"

try:
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)

except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)

def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object

def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print('SAVED: {0!s}'.format(new_settings_file))

    print('Client version: {0!s}'.format(client_version))

try:
    settings_file = settings_file_path
    if not os.path.isfile(settings_file):
        # settings file does not exist
        print('Unable to find file: {0!s}'.format(settings_file))

        # login new
        api = Client(
            user_name, password,
            on_login=lambda x: onlogin_callback(x, settings_file_path))
    else:
        with open(settings_file) as file_data:
            cached_settings = json.load(file_data, object_hook=from_json)
        print('Reusing settings: {0!s}'.format(settings_file))

        device_id = cached_settings.get('device_id')
        # reuse auth settings
        api = Client(
            user_name, password,
            settings=cached_settings)

except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
    print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

    # Login expired
    # Do relogin but use default ua, keys and such
    api = Client(
        user_name, password,
        on_login=lambda x: onlogin_callback(x, settings_file_path))

except ClientLoginError as e:
    print('ClientLoginError {0!s}'.format(e))
    exit(9)
except ClientError as e:
    print('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
    exit(9)
except Exception as e:
    print('Unexpected Exception: {0!s}'.format(e))
    exit(99)

results = api.feed_timeline()
items = [item for item in results.get('feed_items', [])
    if item.get('media_or_ad')]
for item in items:
    # Manually patch the entity to match the public api as closely as possible, optional
    # To automatically patch entities, initialise the Client with auto_patch=True
    ClientCompatPatch.media(item['media_or_ad'])

# Show when login expires
cookie_expiry = api.cookie_jar.auth_expires
print('Cookie Expiry: {0!s}'.format(datetime.datetime.fromtimestamp(cookie_expiry).strftime('%Y-%m-%dT%H:%M:%SZ')))