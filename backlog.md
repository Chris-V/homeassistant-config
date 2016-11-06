# TODOs
## Bugs
- Push Notifications ar enot working at all

## Improvements
### Network devices
- OFF should shut the device down.  
  Contribute to the actual code. turn_off could trigger a service, script, or whatever.    
  https://github.com/home-assistant/home-assistant/blob/dev/homeassistant/components/switch/wake_on_lan.py#L76

## Automations
### automation.network_davice_state
- Should add actions to turn on/off directly from the notif. card. Require push notifications.

### Turn on porch light:
- Add to sunset scene

### Turn on porch light for 5 minutes:
- Scene: Late Arrival
- Household may be home, but not everybody
- Someone arrives AND sun is below_horizon AND time is after midnight

### Turn off porch light:
- Midnight
