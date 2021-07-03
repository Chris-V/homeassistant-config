ATTR_AUDIO = 'audio'
ATTR_DISMISS = 'dismiss'
ATTR_DISMISSIBLE = 'dismissible'
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

HTML_PARAGRAPH_FORMAT = '<p>{}</p>'

audio = data.get(ATTR_AUDIO, False)
dismiss = data.get(ATTR_DISMISS, False)
dismiss = data.get(ATTR_DISMISS, False)
dismissible = data.get(ATTR_DISMISSIBLE, True)
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

if not dismissible and not tag:
    logger.error('Non-dismissible notifications must have a tag.')
    dismissible = True

if not title:
    logger.error(
        'Missing {}. Expected a non-empty string.'
            .format(ATTR_TITLE))
elif dismiss and not tag:
    logger.error('Must provide a tag to dismiss a notification.')
else:
    if push_target:
        payload = {'data': {}}

        if tag:
            payload['data']['tag'] = tag

        if dismiss:
            payload['message'] = 'clear_notification'
        else:
            payload['title'] = title
            payload['message'] = message

            if not dismissible:
                payload['data']['persistent'] = True
                payload['data']['sticky'] = True
            if url:
                payload['data']['url'] = url # Web
                payload['data']['clickAction'] = url # Mobile App
            if priority:
                payload['data']['color'] = '#960000'
                payload['data']['priority'] = 'high'
                payload['data']['ttl'] = 0
                payload['data']['requireInteraction'] = True
                payload['data']['channel'] = 'alarm_stream'
            if push_actions:
                payload['data']['actions'] = push_actions

        for k, v in push_data.items():
            payload['data'][k] = v

        hass.services.call('notify', PUSH_GROUPS[push_target], payload)

    if persistent:
        if dismiss:
            payload = {'notification_id': tag}
            hass.services.call('persistent_notification', 'dismiss', payload)
        else:
            payload = {}
            message_parts = []

            if message:
                payload['title'] = title
                message_parts.append(HTML_PARAGRAPH_FORMAT.format(message))
            else:
                message_parts.append(HTML_PARAGRAPH_FORMAT.format(title))

            if url:
                anchor = '<a href="{}">More details here.</a>'.format(url)
                message_parts.append(HTML_PARAGRAPH_FORMAT.format(anchor))

            if tag:
                payload['notification_id'] = tag

            payload['message'] = '\n'.join(message_parts)

            hass.services.call('persistent_notification', 'create', payload)

    if audio:
        if dismiss:
            payload = {'action': 'pop', 'tag': tag}
            hass.services.call('script', 'manage_broadcast_queue', payload)
        else:
            if priority:
                payload = {
                    'message': 'Alert. {}'.format(message or title)
                }
                hass.services.call('script', 'broadcast_notification', payload)
            else:
                payload = {'action': 'add', 'message': message or title}
                if tag:
                    payload['tag'] = tag

                hass.services.call('script', 'manage_broadcast_queue', payload)
