# TODOs
## Bugs
- Push Notifications are not working at all

## Improvements
### Shell Commands
- Prettycize the usage. Maybe:
   - /home/hass/.homeassistant/includes/shell\_commands/exec.sh "shutdown\_smb" "secret:network\_media\_host" "secret:network\_media\_samba"
      - exec.sh will run $1 with the parameters that follow
      - Parameters prefixed with "secret:" are loaded from secrets.yaml

### Network devices
- WOL for Hue Hub. Note: May not work at all, requires research.

## Automations
### UPS
- Notify when power is down / back up.
- Shutdown media when power is down for 30 seconds.
- Start media when power is back up for 30 seconds.

### automation.network\_davice\_state
- Add notification card actions to turn device on/off. Requires push notifications to work.

### Turn on porch light:
- Add to sunset scene

### Turn on porch light for 5 minutes:
- Scene: Late Arrival
- Household may be home, but not everybody
- Someone arrives AND sun is below\_horizon AND time is after midnight

### Turn off porch light:
- Midnight
