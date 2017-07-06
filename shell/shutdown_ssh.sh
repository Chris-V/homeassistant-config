#!/usr/bin/env bash

ssh "hass@$1" -i "$2" sudo poweroff
