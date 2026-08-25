# Abnormal Procedures

> These procedures are derived from the efis-editor checklist file.

## Abnormal

### Loss of Fuel Pressure

- Fuel Pressure ... **CHECK GREEN**
  
    *should be 45 PSI DIFF; auto-cutover trips when Borla output drops to 22 PSI absolute (Dynon DIFF varies with MAP)*
- Pump 2 Annunciator ... **VERIFY ENGAGED**
  
    *amber on EFII controller — Bus Manager auto-cutover*

#### If Pump 2 not engaged:

- Fuel Pump Mode ... **2**
  
    *manual override*
- Fuel Selector ... **OTHER TANK**
  
    *rules out tank issue*

#### If pressure restored:

- Fuel Pump Mode ... **TRY 1/AUTO**
  
    *if Pump 1 actually failed, Bus Manager auto-cuts back to Pump 2 when Borla output drops to 22 PSI absolute*

#### If Pump 2 fails after a cutover:

- Fuel Pump Switch ... **CYCLE RAPIDLY**
  
    *1/AUTO - 2 - 1/AUTO resets the latch; Pump 1 reactivates*
- Plan Diversion ... **NEAREST SUITABLE**

### Single ECU Failure


*Symptoms: rough running, EGT spread, ECU GRAY/RED on controller.*

- ECU Select ... **OPPOSITE ECU**
- Fuel Trim ... **ADJUST**
  
    *if sensor failure caused rich/lean condition*
- Power ... **REDUCE TO SMOOTH**
- Plan Diversion ... **NEAREST SUITABLE**

> *Note: Once you've identified the bad ECU, do NOT switch back to test.*


### Door Open In Flight


> ⚠️ **WARNING:** FLY THE AIRPLANE FIRST.

- Airspeed ... **SLOW TO ~100 KIAS**
  
    *reduces airflow load on door*
- Door ... **DO NOT ATTEMPT TO CLOSE**
  
    *cannot be re-latched against airflow*
- Occupant ... **BRACE / HOLD**
- Land ... **NEAREST SUITABLE**

### Smoke / Smell Investigation


*Use this when something smells off but no fire is visible.*

- Source ... **ATTEMPT TO IDENTIFY**
  
    *electrical / oil / fuel / hot dust / exhaust*
- Recent Switch Activations ... **NOTE**
  
    *anything just turned on?*
- Vents ... **OPEN**
- Plan Diversion ... **NEAREST SUITABLE**
  
    *do not wait for it to escalate*

> *Note: If smoke or visible fire develops → Electrical Fire / Smoke In Cockpit.*


### CO Alarm In Flight


*CO Guardian audible alarm above 50 PPM. Most likely source: heat muff exhaust crack.*

- Cabin Heat ... **OFF**
- Vents ... **OPEN**
- Oxygen Mask ... **DON / CONSTANT FLOW**
  
    *especially at altitude — CO displaces O2 in blood*
- Land ... **AS SOON AS PRACTICABLE**

> *Note: Have the heat muff and exhaust inspected before next flight.*


### Oxygen System Failure / Hypoxia


*Symptoms: lightheadedness, tunnel vision, fingernails turning blue, fatigue. EDS-4iP not pulsing.*

- O2 Mode Switch ... **EMERGENCY (CONSTANT FLOW, ALL PORTS)**
  
    *panel toggle bypasses pulse-on-demand and supplies all ports continuously*
- Cannulas / Masks ... **VERIFY SEATED**
- Bottle Pressure ... **CHECK**
- Descend ... **BELOW 10,000 FT MSL**
  
    *if symptoms persist, declare and divert*
