#!/usr/bin/env sh

source /var/lib/homeassistant/bin/activate
pip3 install --upgrade homeassistant
deactivate
/var/lib/homeassistant/bin/hass --script check_config
