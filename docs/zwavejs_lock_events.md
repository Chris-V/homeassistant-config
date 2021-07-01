# Lock events

## Summary

Action | `data.type` | `data.event` | `data.event_label` | `data.parameters`
--- | --- | --- | --- | ---
Lock manual | 6 | 1 | Manual lock operation
Unlock manual | 6 | 2 | Manual unlock operation
Lock remote | 6 | 3 | RF lock operation
Unlock remote | 6 | 4 | RF unlock operation
Lock keypad | 6 | 5 | Keypad lock operation
Unlock keypad | 6 | 6 | Keypad unlock operation | `{"userId": 1}`

## Payload

### Unlock manually

```json
{
    "event_type": "zwave_js_notification",
    "data": {
        "domain": "zwave_js",
        "node_id": 00,
        "home_id": 1234567890,
        "device_id": "3083c67ab50c38417a23b483040b8e58",
        "command_class": 113,
        "command_class_name": "Notification",
        "label": "Access Control",
        "type": 6,
        "event": 2,
        "event_label": "Manual unlock operation",
        "parameters": {}
    },
    "origin": "LOCAL",
    "time_fired": "2021-07-01T18:45:33.818016+00:00",
    "context": {
        "id": "ad7777e07cabba93fd6a45db7550c2e8",
        "parent_id": null,
        "user_id": null
    }
}
```

### Lock manually

```json
{
    "event_type": "zwave_js_notification",
    "data": {
        "domain": "zwave_js",
        "node_id": 00,
        "home_id": 1234567890,
        "device_id": "3083c67ab50c38417a23b483040b8e58",
        "command_class": 113,
        "command_class_name": "Notification",
        "label": "Access Control",
        "type": 6,
        "event": 1,
        "event_label": "Manual lock operation",
        "parameters": {}
    },
    "origin": "LOCAL",
    "time_fired": "2021-07-01T18:47:46.024526+00:00",
    "context": {
        "id": "04b8e69bb37548fc1419803647e95acd",
        "parent_id": null,
        "user_id": null
    }
}
```

### Unlock remotely

```json
{
    "event_type": "zwave_js_notification",
    "data": {
        "domain": "zwave_js",
        "node_id": 00,
        "home_id": 1234567890,
        "device_id": "3083c67ab50c38417a23b483040b8e58",
        "command_class": 113,
        "command_class_name": "Notification",
        "label": "Access Control",
        "type": 6,
        "event": 4,
        "event_label": "RF unlock operation",
        "parameters": {}
    },
    "origin": "LOCAL",
    "time_fired": "2021-07-01T18:48:35.504095+00:00",
    "context": {
        "id": "e56a370d8c6b43a6bb93b03ea9d8b515",
        "parent_id": null,
        "user_id": null
    }
}
```

### Lock remotely

```json
{
    "event_type": "zwave_js_notification",
    "data": {
        "domain": "zwave_js",
        "node_id": 00,
        "home_id": 1234567890,
        "device_id": "3083c67ab50c38417a23b483040b8e58",
        "command_class": 113,
        "command_class_name": "Notification",
        "label": "Access Control",
        "type": 6,
        "event": 3,
        "event_label": "RF lock operation",
        "parameters": {}
    },
    "origin": "LOCAL",
    "time_fired": "2021-07-01T18:49:01.352833+00:00",
    "context": {
        "id": "05abee572d3eac3235da94617fc145b5",
        "parent_id": null,
        "user_id": null
    }
}
```

### Unlock with valid code

```json
{
    "event_type": "zwave_js_notification",
    "data": {
        "domain": "zwave_js",
        "node_id": 00,
        "home_id": 1234567890,
        "device_id": "3083c67ab50c38417a23b483040b8e58",
        "command_class": 113,
        "command_class_name": "Notification",
        "label": "Access Control",
        "type": 6,
        "event": 6,
        "event_label": "Keypad unlock operation",
        "parameters": {
            "userId": 1
        }
    },
    "origin": "LOCAL",
    "time_fired": "2021-07-01T18:50:08.185105+00:00",
    "context": {
        "id": "2a3631c98cd0fa84cb0c1d9d6bc1c975",
        "parent_id": null,
        "user_id": null
    }
}
```

### Unlock with invalid code

No events

### Lock outside

```json
{
    "event_type": "zwave_js_notification",
    "data": {
        "domain": "zwave_js",
        "node_id": 00,
        "home_id": 1234567890,
        "device_id": "3083c67ab50c38417a23b483040b8e58",
        "command_class": 113,
        "command_class_name": "Notification",
        "label": "Access Control",
        "type": 6,
        "event": 5,
        "event_label": "Keypad lock operation",
        "parameters": {}
    },
    "origin": "LOCAL",
    "time_fired": "2021-07-01T18:49:54.304123+00:00",
    "context": {
        "id": "bbab4768ac60631559eaf38221847a00",
        "parent_id": null,
        "user_id": null
    }
}
```
