#!/usr/bin/env sh

source /srv/homeassistant/bin/activate
pip3 install --upgrade homeassistant
deactivate
/srv/homeassistant/bin/hass --script check_config
