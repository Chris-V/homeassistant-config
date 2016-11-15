# TODOs
## Improvements
- WOL for Hue Hub. Note: May not work at all, requires research.

## Automations
### UPS
- Notify when battery must be replaced ('STATUS' contains 'REPLACEBATT')
- Shutdown media when power is down for 70 seconds.
   - UPS is polled every 60 secs, so the poweroff *must* be higher than that or we risk shutting down for short power outages.
- Start media when power is back up for 30 seconds.

### Turn on porch light:
- Add to sunset scene

### Turn on porch light for 5 minutes:
- Scene: Late Arrival
- Household may be home, but not everybody
- Someone arrives AND sun is below\_horizon AND time is after midnight

### Turn off porch light:
- Midnight
