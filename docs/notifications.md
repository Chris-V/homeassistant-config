## Targets 

* Push notifications. Groups:
  * Admin (A)
  * Household (H)
* Persistent. Everybody
* Audio. Everybody
  * Only if household is home

The `alert` component is an option, although is only support notify groups: https://www.home-assistant.io/components/alert/ 

## Notifications

|    | Activity | Tag | Push | Persistent | Audio | Notes
|----|:---------|:----|:----:|:----------:|:-----:|:-----
| 1  | HASS started | hass_state | A | | |
| 1  | HASS stopped | hass_state | A | | |
| 1  | Z-Wave ready | zwave_state | A | | |
| 1  | Z-Wave complete | zwave_state | A | | |
| 2  | Household person arrives | _person_name_ | A | | |
| 2  | Household person leaves | _person_name_ | A | | |
| 3  | Network device off | _device_name_ | A | | |
| 3  | Network device on | _device_name_ | A | | | See about calculating offline time as well. 
| -  | Power outage started | _outage_id_ | H | Y | | Outage id is a timestamp stored in a `input_text.power_outage_id` entity.
| -  | Power outage done | _outage_id_ | H | Y | | Also clear `input_text.power_outage_id`'s value.
| -  | HASS new version | hass_version | A | Y | |
| -  | New device on network | | A | Y | Y |
| -  | Login attempt | | A | Y | Y |
| -  | Change UPS battery | ups_battery | A | Y | |
| -  | Plant problems | _plant_name_ | H | Y | Y |
| -  | Water leaks | _sensor_name_ | H | Y | Y |
| 6  | Door left open | _door_name_ | H | | Y | Loop every 30 seconds.
| 7  | Weather alert | weather_alert | H | Y | Y | Loop every 1 hour.
| -  | Low battery | _battery_name_ | H | Y | |

---

Notification groups:

1. Off by default.
2. Off by default.
3. On by default.
4. On by default.
5. On by default. Resets to on after 24 hours.
6. On by default. Resets to on after 30 minutes.
7. On by default. Resets to on after 24 hours.
