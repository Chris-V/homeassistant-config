# Climate
## Settings

Thermostat     | Economy | Comfort
---------------|---------|--------
Living room    | 16 °C   | 20 °C
Dining room    | 16 °C   | 20 °C
Master Bedroom | 16 °C   | 20 °C
Office         | 16 °C   | 20 °C
Down. hallway  | 16 °C   | 20 °C
Down. bathroom | 16 °C   | 20 °C
Lounge         | 16 °C   | 20 °C
Guest bedroom  | 16 °C   | 20 °C
Studio         | 16 °C   | 20 °C

## Climate Presets (scripts / scenes)

* Away
  * Everywhere: Economy
* Active
  * Everywhere: Comfort
* Bedtime
  * Everywhere: Economy
  * Master Bedroom: Comfort
* Sleep
  * Everywhere: Economy

## Schedule preset

*If unspecified, the last specified preset is implicit.*

Day | 6:30   | 7:30   | 23:00   | 24:00
----|--------|--------|---------|------
Mon | Active |        | Bedtime | Sleep
Tue | Active |        | Bedtime | Sleep
Wed | Active |        | Bedtime | Sleep
Thu | Active |        | Bedtime | Sleep
Fri | Active |        | Bedtime | Sleep
Sat | Active |        | Bedtime | Sleep
Sun |        | Active | Bedtime | Sleep

## Automations

Triggers                             | Conditions                            | Preset
-------------------------------------|---------------------------------------|-----------------
<li>Househould away                  | <li>Guest mode off                    | Away
<li>Household home <li>Every 15m     | <li>Household home                    | Schedule
<li>Bedtime script                   | <li>Guest mode off <li>Household home | Bedtime
<li>Climate preset changed to "None" |                                       | Restore setpoint

## Gotchas
1. Built-in eco setpoint is controlled physically only
  * We will not use built-in preset
  * Updating the preset form HA automatically selects the default hardware preset
