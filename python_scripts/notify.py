ATTR_AUDIO = 'audio'
ATTR_MESSAGE = 'message'
ATTR_PERSISTENT = 'persistent'
ATTR_PRIORITY = 'priority'
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

audio = data.get(ATTR_AUDIO, False)
message = data.get(ATTR_MESSAGE, '')
persistent = data.get(ATTR_PERSISTENT, False)
priority = data.get(ATTR_PRIORITY, False)
push_actions = data.get(ATTR_PUSH_ACTIONS)
push_data = data.get(ATTR_PUSH_DATA, {})
push_target = data.get(ATTR_PUSH_TARGET)
tag = data.get(ATTR_TAG)
title = data.get(ATTR_TITLE)
url = data.get(ATTR_URL)

if not push_target and not persistent and not audio:
    logger.error(
        'Missing notification channel. Expected one of "{}", "{}" or "{}".'
            .format(ATTR_PUSH_TARGET, ATTR_PERSISTENT, ATTR_AUDIO))

if push_target and push_target not in PUSH_GROUPS:
    logger.error(
        'Invalid {}. Expected one of "{}", got "{}".'.format(
            ATTR_PUSH_TARGET,
            '", "'.join(PUSH_GROUPS.keys()),
            push_target))
    push_target = None

if not title:
    logger.error(
        'Missing {}. Expected a non-empty string.'
            .format(ATTR_TITLE))
else:
    if push_target:
        payload = {'title': title, 'message': message, 'data': {}}

        for k, v in push_data.items():
            payload['data'][k] = v

        if tag:
            payload['data']['tag'] = tag
        if url:
            payload['data']['url'] = url # Web
            payload['data']['clickAction'] = url # Mobile App
        if priority:
            payload['data']['color'] = '#960000'
            payload['data']['priority'] = 'high'
            payload['data']['requireInteraction'] = True
        if push_actions:
            payload['data']['actions'] = push_actions

        hass.services.call('notify', PUSH_GROUPS[push_target], payload)

    if persistent:
        payload = {}
        message_parts = []

        if message:
            payload['title'] = title
            message_parts.append(message)
        else:
            message_parts.append(title)

        if url:
            message_parts.append(
                '<a href="{}"> More details here.</a>'.format(url))

        if tag:
            payload['notification_id'] = tag

        payload['message'] = "\n\n".join(message_parts)

        hass.services.call('persistent_notification', 'create', payload)

    if audio:
        if priority:
            payload = {
                'message': 'Alert. {}'.format(message or title)
            }
            hass.services.call('script', 'broadcast_notification', payload)
        else:
            payload = {
                'object_id': 'broadcast_notifications',
                'data': message or title
            }
            hass.services.call('custom_storage', 'add', payload)
