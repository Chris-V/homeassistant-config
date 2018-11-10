"""Component to manage key-value data using CRUD operations."""
import logging
import os
import uuid

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import ATTR_ID
from homeassistant.helpers.entity import Entity, async_generate_entity_id
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.util.json import save_json, load_json

DOMAIN = 'custom_storage'

ENTITY_ID_FORMAT = DOMAIN + '.{}'

CONF_PERSISTENCE = 'enable_persistence'

ATTR_DATA = 'data'
ATTR_OBJECT_ID = 'object_id'

SERVICE_ADD = 'add'
SERVICE_CLEAR = 'clear'
SERVICE_REMOVE = 'remove'
SERVICE_UPDATE = 'update'

ADD_SERVICE_SCHEMA = vol.Schema({
    vol.Required(ATTR_OBJECT_ID): cv.slug,
    vol.Required(ATTR_DATA): cv.string
})

CLEAR_SERVICE_SCHEMA = vol.Schema({
    vol.Required(ATTR_OBJECT_ID): cv.slug
})

REMOVE_SERVICE_SCHEMA = vol.Schema({
    vol.Required(ATTR_OBJECT_ID): cv.slug,
    vol.Required(ATTR_ID): cv.string
})

UPDATE_SERVICE_SCHEMA = vol.Schema({
    vol.Required(ATTR_OBJECT_ID): cv.slug,
    vol.Required(ATTR_ID): cv.string,
    vol.Required(ATTR_DATA): cv.string
})

PERSISTENCE_PATH = '.custom_storage'
_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        cv.slug: vol.Any({
            vol.Optional(CONF_PERSISTENCE, default=False): cv.boolean,
        })
    })
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass, config):
    """Initialize the shopping list."""
    component = hass.data.get(DOMAIN)

    if component is None:
        component = hass.data[DOMAIN] = EntityComponent(_LOGGER, DOMAIN, hass)

    entities = [await _create_storage_entity(hass, object_id, conf)
                for object_id, conf in config.get(DOMAIN, {}).items()]
    await component.async_add_entities(entities, True)

    async def add_service_handler(service):
        """Add an item with `data`."""
        object_id = service.data[ATTR_OBJECT_ID]
        entity_id = ENTITY_ID_FORMAT.format(object_id)
        storage = component.get_entity(entity_id)

        item_data = service.data.get(ATTR_DATA)

        item = await storage.add_item(item_data)
        if item is not None:
            storage.schedule_update_ha_state()

    hass.services.async_register(
        DOMAIN, SERVICE_ADD, add_service_handler,
        schema=ADD_SERVICE_SCHEMA)

    async def clear_service_handler(service):
        """Remove all items."""
        object_id = service.data[ATTR_OBJECT_ID]
        entity_id = ENTITY_ID_FORMAT.format(object_id)
        storage = component.get_entity(entity_id)

        cleared = await storage.clear()
        if cleared:
            storage.schedule_update_ha_state()

    hass.services.async_register(
        DOMAIN, SERVICE_CLEAR, clear_service_handler,
        schema=CLEAR_SERVICE_SCHEMA)

    async def remove_service_handler(service):
        """Remove the item identified with `id`."""
        object_id = service.data[ATTR_OBJECT_ID]
        entity_id = ENTITY_ID_FORMAT.format(object_id)
        storage = component.get_entity(entity_id)

        item_id = service.data.get(ATTR_ID)

        removed = await storage.remove_item(item_id)

        if removed:
            storage.schedule_update_ha_state()
        else:
            _LOGGER.error("Removal of item failed: %s cannot be found",
                          item_id)

    hass.services.async_register(
        DOMAIN, SERVICE_REMOVE, remove_service_handler,
        schema=REMOVE_SERVICE_SCHEMA)

    async def update_service_handler(service):
        """Update an item identified with `id` with `data`."""
        object_id = service.data[ATTR_OBJECT_ID]
        entity_id = ENTITY_ID_FORMAT.format(object_id)
        storage = component.get_entity(entity_id)

        item_id = service.data.get(ATTR_ID)
        item_data = service.data.get(ATTR_DATA)

        item = await storage.update_item(item_id, item_data)
        if item is not None:
            storage.schedule_update_ha_state()

    hass.services.async_register(
        DOMAIN, SERVICE_UPDATE, update_service_handler,
        schema=UPDATE_SERVICE_SCHEMA)

    return True


async def _create_storage_entity(hass, object_id, conf):
    persistence = conf.get(CONF_PERSISTENCE)
    persistence_file = None
    items = []

    if persistence:
        items, persistence_file = _load_items(hass, object_id)

    entity = Storage(hass, items, persistence_file)
    entity.entity_id = async_generate_entity_id(
        ENTITY_ID_FORMAT, object_id, hass=hass)

    return entity


def _load_items(hass, object_id):
    items = []
    persistence_path = hass.config.path(PERSISTENCE_PATH)
    persistence_file = os.path.join(persistence_path, object_id + '.json')

    if os.path.exists(persistence_file):
        items = load_json(persistence_file, [])
    else:
        if not os.path.exists(persistence_path):
            os.makedirs(persistence_path)

        file = open(persistence_file, 'w')
        file.write('[]')
        file.close()

    return items, persistence_file


class Storage(Entity):
    def __init__(self, hass, items, persistence_file):
        self.hass = hass
        self._items = items
        self._persistence_file = persistence_file

        self._refresh_state()

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def state(self) -> str:
        return self._state

    @property
    def state_attributes(self):
        return self._attributes

    async def clear(self):
        """Remove all items from the collection."""
        if len(self._items) != 0:
            self._items = []
            self._refresh_state()
            await self._maybe_persist()

            return True

        return False

    async def add_item(self, data):
        """Add an item to the collection and generate a unique id."""
        if not isinstance(data, str) or len(data.strip()) == 0:
            return None

        item = {
            'id': uuid.uuid4().hex,
            'data': data
        }

        self._items.append(item)
        self._refresh_state()
        await self._maybe_persist()

        return item

    async def remove_item(self, item_id):
        """Remove the item with `item_id`."""
        new_items = [item for item in self._items if item['id'] != item_id]

        if len(new_items) != len(self._items):
            self._items = new_items
            self._refresh_state()
            await self._maybe_persist()

            return True

        return False

    async def update_item(self, item_id, data):
        """Update the item with `item_id`."""
        item = next((item for item in self._items if item['id'] == item_id),
                    None)

        if item:
            item['data'] = data
            self._refresh_state()
            await self._maybe_persist()

        return item

    def _refresh_state(self):
        attributes = {'size': len(self._items)}

        for idx, item in enumerate(self._items):
            key_prefix = 'item_{0}_'.format(idx)
            attributes[key_prefix + 'id'] = item['id']
            attributes[key_prefix + 'data'] = item['data']

        self._attributes = attributes
        self._state = self._items[0]['data'] if attributes['size'] != 0 else ''

    async def _maybe_persist(self):
        if self._persistence_file:
            await self.hass.async_add_job(save_json,
                                          self._persistence_file,
                                          self._items)
