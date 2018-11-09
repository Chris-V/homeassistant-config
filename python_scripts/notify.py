ATTR_AUDIO = 'audio'
ATTR_MESSAGE = 'message'
ATTR_PERSISTENT = 'persistent'
ATTR_PUSH_ACTIONS = 'push_actions'
ATTR_PUSH_DATA = 'push_data'
ATTR_PUSH_TARGET = 'push_target'
ATTR_TAG = 'tag'
ATTR_TITLE = 'title'
ATTR_URL = 'url'

ATTR_ADMIN_TARGET = 'admin'
ATTR_HOUSEHOLD_TARGET = 'household'

PUSH_GROUPS = {
    ATTR_ADMIN_TARGET: 'admin',
    ATTR_HOUSEHOLD_TARGET: 'household',
}
TTS_ENTITIES = ['media_player.living_room_google_home']

audio = data.get(ATTR_AUDIO, False)
message = data.get(ATTR_MESSAGE, '')
persistent = data.get(ATTR_PERSISTENT, False)
push_actions = data.get(ATTR_PUSH_ACTIONS)
push_data = data.get(ATTR_PUSH_DATA, {})
push_target = data.get(ATTR_PUSH_TARGET)
tag = data.get(ATTR_TAG)
title = data.get(ATTR_TITLE)
url = data.get(ATTR_URL)

if not title:
    logger.error('Missing {}. Expected a non-empty string.'.format(ATTR_TITLE))
    title = 'Home Assistant'

if push_target and push_target not in PUSH_GROUPS:
    logger.error('Invalid {}. Expected one of "{}", got "{}".'
                 .format(ATTR_PUSH_TARGET,
                         '", "'.join(PUSH_GROUPS.keys()),
                         push_target))
    push_target = None

if not push_target and not persistent and not audio:
    logger.error(
        'Missing notification channel. Expected one of "{}", "{}" or "{}".'
            .format(ATTR_PUSH_TARGET, ATTR_PERSISTENT, ATTR_AUDIO))

if push_target:
    payload = {'title': title, 'message': message, 'data': {}}

    for k, v in push_data.items():
        payload['data'][k] = v

    if tag:
        payload['data']['tag'] = tag
    if url:
        payload['data']['url'] = url
    if push_actions:
        payload['data']['actions'] = push_actions

    hass.services.call('notify', PUSH_GROUPS[push_target], payload)

if persistent:
    payload = {'title': title}

    message_parts = [message]
    if url:
        message_parts.append(
            '<a href="{}"> More details here.</a>'.format(url))
    payload['message'] = "\n\n".join(message_parts)

    if tag:
        payload['notification_id'] = tag

    hass.services.call('persistent_notification', 'create', payload)

if audio:
    payload = {'language': 'en', 'message': '. '.join([title, message])}
    for entity_id in TTS_ENTITIES:
        payload['entity_id'] = entity_id
        hass.services.call('tts', 'google_say', payload)