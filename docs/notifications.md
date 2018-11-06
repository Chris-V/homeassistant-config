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
| 1  | HASS started | hass\_state | A | N | N |
| 1  | HASS stopped | hass\_state | A | N | N |
| 1  | Z-Wave ready | zwave\_state | A | N | N |
| 1  | Z-Wave complete | zwave\_state | A | N | N |
| -  | HASS new version | hass\_version | A | Y | N |
| 2  | Household person arrives | presence\__person_name_ | A | N | N |
| 2  | Household person leaves | presence\__person_name_ | A | N | N |
| 3  | Network device off | device\_outage\__device_name_ | A | N | N |
| 3  | Network device on | device\_outage\__device_name_ | A | N | N | See about calculating offline time as well. 
| -  | Power outage started | power\_outage\__outage_id_ | H | Y | N | Outage id is a timestamp stored in a `input_text.power_outage_id` entity.
| -  | Power outage done | power\_outage\__outage_id_ | H | Y | N | Also clear `input_text.power_outage_id`'s value.
| -  | New device on network | - | A | Y | N |
| -  | Login attempt | - | A | Y | N |
| -  | Plant problems | plant\__plant_name_ | H | Y | Y |
| -  | Water leaks | water\__sensor_name_ | H | Y | Y |
| 6  | Door left open | door\__door_name_ | H | N | Y | Loop every 30 seconds.
| 7  | Weather alert | weather\_alert | H | Y | Y | Loop every 1 hour.
| -  | Low battery | battery\_low\__battery_name_ | H | Y | N |

---

Notification groups:

1. Off by default.
2. Off by default.
3. On by default.
4. On by default.
5. On by default. Resets to on after 24 hours.
6. On by default. Resets to on after 30 minutes.
7. On by default. Resets to on after 24 hours.
