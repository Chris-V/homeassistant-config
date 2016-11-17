"""
Support for Tomato routers.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/device_tracker.tomato/
"""
import json
import logging
import re
import threading
from datetime import timedelta

import requests
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.device_tracker import DOMAIN, PLATFORM_SCHEMA
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.util import Throttle

# Return cached results if last scan was less then this time ago.
MIN_TIME_BETWEEN_SCANS = timedelta(seconds=5)

CONF_HTTP_ID = "http_id"
CONF_MIN_QUALITY = "minimum_quality"

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_HTTP_ID): cv.string,
    vol.Optional(CONF_MIN_QUALITY, default=0): cv.positive_int
})


def get_scanner(hass, config):
    """Validate the configuration and returns a Tomato scanner."""
    return TomatoDeviceScanner(config[DOMAIN])


class TomatoDeviceScanner(object):
    """This class queries a wireless router running Tomato firmware."""

    def __init__(self, config):
        """Initialize the scanner."""
        host, http_id = config[CONF_HOST], config[CONF_HTTP_ID]
        username, password = config[CONF_USERNAME], config[CONF_PASSWORD]

        self.minimum_quality = config[CONF_MIN_QUALITY]

        self.req = requests.Request('POST',
                                    'http://{}/update.cgi'.format(host),
                                    data={'_http_id': http_id,
                                          'exec': 'devlist'},
                                    auth=requests.auth.HTTPBasicAuth(
                                        username, password)).prepare()

        self.parse_api_pattern = re.compile(r"(?P<param>\w*) = (?P<value>.*);")

        self.logger = logging.getLogger("{}.{}".format(__name__, "Tomato"))
        self.lock = threading.Lock()

        self.last_results = {"wldev": [], "dhcpd_lease": [], "wlnoise": []}

        self.success_init = self._update_tomato_info()

    def scan_devices(self):
        """Scan for new devices and return a list with found device IDs."""
        self._update_tomato_info()

        return [item[1] for item in self.last_results['wldev']
                if item[2] - self.last_results['wlnoise'][item[6]]
                >= self.minimum_quality]

    def get_device_name(self, device):
        """Return the name of the given device or None if we don't know."""
        filter_named = [item[0] for item in self.last_results['dhcpd_lease']
                        if item[2] == device]

        if not filter_named or not filter_named[0]:
            return None
        else:
            return filter_named[0]

    @Throttle(MIN_TIME_BETWEEN_SCANS)
    def _update_tomato_info(self):
        """Ensure the information from the Tomato router is up to date.

        Return boolean if scanning successful.
        """
        with self.lock:
            self.logger.info("Scanning")

            try:
                response = requests.Session().send(self.req, timeout=3)
                # Calling and parsing the Tomato api here. We only need the
                # wldev and dhcpd_lease values.
                if response.status_code == 200:

                    for param, value in \
                            self.parse_api_pattern.findall(response.text):

                        if param in self.last_results.keys():
                            self.last_results[param] = \
                                json.loads(value.replace("'", '"'))
                    return True

                elif response.status_code == 401:
                    # Authentication error
                    self.logger.exception((
                        "Failed to authenticate, "
                        "please check your username and password"))
                    return False

            except requests.exceptions.ConnectionError:
                # We get this if we could not connect to the router or
                # an invalid http_id was supplied.
                self.logger.exception((
                    "Failed to connect to the router"
                    " or invalid http_id supplied"))
                return False

            except requests.exceptions.Timeout:
                # We get this if we could not connect to the router or
                # an invalid http_id was supplied.
                self.logger.exception(
                    "Connection to the router timed out")
                return False

            except ValueError:
                # If JSON decoder could not parse the response.
                self.logger.exception(
                    "Failed to parse response from router")
                return False
