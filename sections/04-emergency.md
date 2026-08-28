# Emergency Procedures

> These procedures are derived from the efis-editor checklist file.
> Update the source JSON and regenerate to modify.

## Engine Failures

### System32 Restore Function


*Run any time the engine is rough, faltering, or has quit.*

- Controller Dark? ... **EMERG PWR ON**
  
    *a dark EFII controller means power failure, not logic — E-pwr restores the essential bus; then continue*
- ECU Select ... **OPPOSITE ECU**
  
    *shifts fuel control to the other ECU; sensors are independent*
- Fuel Pump Mode ... **2**
  
    *covers a delivery fault that never tripped the 22 PSI auto-cutover*
- Fuel Selector ... **OTHER TANK / VERIFY ON**
- Fuel Pump Breakers ... **BOTH IN**
- Fuel Trim ... **ADJUST**
  
    *if engine firing but rough — try richer (CW) then leaner*
- Emergency Power Switch ... **ON**
  
    *catch-all — bypasses the Bus Manager even when the panel looks alive*

### Engine Failure During Takeoff Run

- Throttle ... **IDLE**
- Brakes ... **APPLY**
- Stop ... **STRAIGHT AHEAD**
- Wing Flaps ... **RETRACT**
- Fuel Selector ... **OFF**
- Key Switch ... **OFF**

### Engine Failure Immediately After Takeoff


**Pitch** ... **ONSPEED**


**Landing Spot** ... **WITHIN ±30º**


  *above turnback altitude / per TLAR — see Turnback Procedure*

- ECU Select ... **OPPOSITE ECU**
  
    *one shot — if no restart, commit to landing*
- Fuel Selector ... **OFF**
- Key Switch ... **OFF**
- Wing Flaps ... **AS REQUIRED**
  
    *33º on short final*
- Doors ... **UNLATCH PRIOR TO TOUCHDOWN**

### Engine Failure In Flight


**Airspeed** ... **BEST GLIDE 95 KIAS**


**NRST Button** ... **HOLD / AP ENGAGE**


  *AP flies to nearest field at best glide; tunes comms*


**Best Field** ... **DECIDE**


  *is the nearest field actually best? terrain, wind, surface*

- System32 Restore Function ... **EXECUTE**
  
    *Ctrl dark→E-Pwr / ECU Sel / Pump 2 / Fuel Sel / Brkrs / Trim / E-Pwr*

#### If engine restored:

- Continue to Nearest Suitable ... **MONITOR**
  
    *do not switch back to test — leave the bad ECU off*

#### If engine not restored:

- Forced Landing ... **EXECUTE**
  
    *as described in Emergency Landing Without Engine Power*

### Engine Failure On Approach


**Airspeed** ... **ONSPEED**


  *best glide gives more distance, but already configured for landing*


**Best Surface** ... **LAND**


  *may not be the runway — pick what works*

- ECU Select ... **OPPOSITE ECU**
  
    *if time / altitude permits — one shot*
- Fuel Selector ... **OFF**
- Key Switch ... **OFF**
- Doors ... **UNLATCH PRIOR TO TOUCHDOWN**

## Forced Landings

### Emergency Landing Without Engine Power

- Squawk ... **7700**
- Airspeed ... **BEST GLIDE / ONSPEED**
  
    *95 KIAS clean / ONSPEED with flaps*
- Fuel Selector ... **OFF**
- Key Switch ... **OFF**
  
    *kills ECUs; engine dies clean*
- Wing Flaps ... **AS REQUIRED — 40º RECOMMENDED**
- Radio Call ... **MAYDAY 121.5**
  
    *time permitting*
- Doors ... **UNLATCH PRIOR TO TOUCHDOWN**
- Touchdown ... **SLIGHTLY TAIL LOW**
- Brakes ... **APPLY HEAVILY**

### Turnback Procedure


*Decided on the ground per pre-takeoff brief.*


> ⚠️ **WARNING:** Below 200 ft AGL, turnback is non-recoverable. Land ahead.

- Pitch ... **ONSPEED IMMEDIATELY**
  
    *single AOA reference — best blend of turn rate and stall margin*
- Turn Direction ... **INTO CROSSWIND**
  
    *wind drifts you toward centerline during reversal*
- Bank ... **45º**
  
    *any less wastes altitude; any more loses stall margin*
- Coordinate ... **BALL CENTERED**
  
    *uncoordinated stall is non-recoverable at low altitude*
- On Speed ... **MAINTAIN TO TOUCHDOWN**

> *Note: If turn not working: WINGS LEVEL, LAND AHEAD AS SLOW AS POSSIBLE.*


*Don't stall. Everything else is secondary.*


### Precautionary Landing With Engine Power


*Lowest sustainable energy at touchdown — drag it in with power.*

- Airspeed ... **ONSPEED**
- Wing Flaps ... **16º**
- Selected Field ... **FLY OVER**
- Terrain And Obstructions ... **NOTE**
- Wing Flaps (On Final) ... **33º**
- Airspeed ... **SLOW TONE**
- Power ... **CONTROL DESCENT RATE**
- Avionics Master ... **OFF**
- Doors ... **UNLATCH PRIOR TO TOUCHDOWN**
- Touchdown ... **SLIGHTLY TAIL LOW**
- Key Switch ... **OFF**
- Brakes ... **APPLY HEAVILY**

### Ditching


*Goal is lowest sustainable energy at touchdown — fly the slow tone.*

- Transmit Mayday ... **121.5 MHZ, GIVING LOCATION**
- Squawk ... **7700**
- Heavy Objects ... **SECURE OR JETTISON**
- Flaps ... **16º - 33º**
- Power ... **ESTABLISH 300 FT/MIN DESCENT, SLOW TONE**

#### Approach:


  *High Winds, Heavy Seas — INTO THE WIND*


  *Light Winds, Heavy Swells — PARALLEL TO SWELLS*

- Cabin Doors ... **UNLATCH**
- Touchdown ... **LEVEL ATTITUDE AT ESTABLISHED DESCENT**
- Airplane ... **EVACUATE**
- Life Vests and Raft ... **INFLATE**

### Landing With A Flat Main Tire

- Approach ... **NORMAL**
- Wing Flaps ... **FULL DOWN**
- Touchdown ... **GOOD TIRE FIRST**
  
    *hold airplane off flat tire as long as possible with aileron*

### Landing Without Elevator Control

- Airspeed ... **80 KIAS**
- Elevator Trim ... **LEVEL FLIGHT**
- Glide Angle ... **CONTROL WITH POWER**
- Elevator Trim ... **FULL NOSE UP**
  
    *in flare — rotates to horizontal for touchdown*
- Throttle ... **CLOSE AT TOUCHDOWN**

## Fires

### Engine Fire During Start On Ground


#### If engine starts:

- Fuel Pump Breakers ... **PULL BOTH**
  
    *stop feeding the fire — the engine runs a few seconds on residual rail pressure*
- Throttle ... **OPEN SLOWLY / 1800 RPM**
  
    *slow push — a fast one fires the accelerator-pump squirt; airflow purges the intake until the engine starves and dies*
- Key Switch ... **OFF**
  
    *after the engine dies*
- Fuel Selector ... **OFF**
- Doors ... **UNLATCH**
- Evacuate / Extinguisher ... **AS REQUIRED**

#### If engine fails to start:

- Fuel Pump Breakers ... **PULL BOTH**
  
    *fuel off FIRST — cranking with the pumps on floods the intake and feeds the fire*
- Throttle ... **OPEN / DO NOT PUMP**
  
    *pumping the throttle fires the primer squirt*
- Starter ... **CRANK ~10 SECONDS**
  
    *purge crank — injectors run dry in seconds once the pumps are off. Key stays ON: the starter is dead with the key off*
- Key Switch ... **OFF**
- Emergency Power Switch ... **OFF**
  
    *E-pwr re-powers the ECUs and the starter — must be off*
- Fuel Selector ... **OFF**
- Doors ... **UNLATCH**
- Fire Extinguisher ... **AS REQUIRED**
- Evacuate ... **IMMEDIATELY**

### Engine Fire In Flight


**Fuel Pump Breakers** ... **PULL BOTH**


  *the pumps are the 45 PSI feeding a fuel fire — physical breakers beat switch logic in a fire*


**Key Switch** ... **OFF**


  *kills ECUs, both busses, and any wire-arc source*


**Fuel Selector** ... **OFF**


  *stops gravity/siphon feed to a firewall-forward leak*

- Emergency Power Switch ... **OFF**
  
    *E-pwr independently re-powers ECUs and pumps — both paths must be off*
- Cabin Heat / Air ... **OFF**
  
    *close firewall vents*
- Airspeed ... **INCREASE**
  
    *slip or dive to blow out fire*
- Forced Landing ... **EXECUTE IMMEDIATELY**

#### If fire not extinguished:

- Sideslip ... **INTO FIRE SIDE**
  
    *keep flames away from cabin*
- Land ... **IMMEDIATELY**

### Electrical Fire / Smoke In Cockpit


**Key Switch** ... **OFF**


  *the one keyed master — kills ECUs, fuel pumps, and both busses*


**Emergency Power Switch** ... **OFF**


  *now the airplane is fully dark*


**Vents / Cabin Air** ... **OPEN**


  *clear smoke*

- Fire Extinguisher ... **AS REQUIRED**
- Land ... **AS SOON AS PRACTICABLE**

#### If engine required to reach landing site:

- Emergency Power Switch ... **ON**
  
    *restores engine power only — non-essential systems stay dead*
- Monitor ... **FOR RECURRENCE**

> *Note: If smoke returns, Emergency Power → OFF and re-isolate.*


### Cabin Fire

- Fire Electrical? ... **USE ELECTRICAL FIRE CL**
  
    *killing the key stops the engine — isolate electrics only if the fire IS electrical*
- Vents / Cabin Air / Heat ... **CLOSED**
- Fire Extinguisher ... **ACTIVATE**

> ⚠️ **WARNING:** After discharging an extinguisher in a closed cabin, ventilate the cabin.

- Land ... **AS SOON AS POSSIBLE**
- Airplane ... **INSPECT FOR DAMAGE**

### Wing Fire

- Navigation Light ... **OFF**
- Strobe Light ... **OFF**
- Pitot Heat ... **OFF**

> *Note: Sideslip to keep flames away from fuel tank and cabin. Land as soon as possible. Flaps only as required for final approach and touchdown.*


## Electrical / Engine Malfunctions

### Primary Alternator (Hartzell) Failure


*Symptoms: Bat 1 voltage dropping, alternator amps zero, low-voltage indication.*

- Bat 1 Voltage ... **CHECK**
- Alternator Field Switch ... **CYCLE OFF / ON**
  
    *one attempt only*

#### If still failed:

- Non-Essential Loads ... **REDUCE**
  
    *VPX may auto-shed; help it*
- MZ-30 ... **VERIFY OPERATING**
  
    *Bat 2 voltage holding, generator amps positive*
- Plan Diversion ... **NEAREST SUITABLE**
  
    *Bat 1 will eventually drain even with reduced load*

#### If Bat 1 voltage critical:

- Emergency Power Switch ... **ON**
  
    *moves essential bus to Bat 2 / MZ-30*

### MZ-30 Generator Failure


*Symptoms: Bat 2 voltage dropping, generator amps zero or low.*

- MZ-30 Enable Switch ... **VERIFY ON**
- Generator Amps ... **CHECK**
  
    *expect 5-30A in normal operation*
- Bat 2 Voltage ... **MONITOR**

#### If still failed:

- MZ-30 Enable Switch ... **OFF**
  
    *regulator may have OVP-locked; disable to prevent damage*
- Continue on Hartzell / Bat 1 ... **FLIGHT NOT AT RISK**
  
    *Plan return when convenient — primary system intact*

### Bus Manager Failure / Switch to Endurance Bus


*Symptoms: multiple essential systems unresponsive; primary bus dead.*


**Emergency Power Switch** ... **ON**


  *bypasses Bus Manager — connects Bat 2 / MZ-30 directly to essential bus*

- Non-Essential Loads ... **OFF**
- Squawk ... **7700**
- Mayday Call ... **121.5**
- Land ... **AS SOON AS PRACTICABLE**

> ⚠️ **WARNING:** If Emergency Power does not restore essential bus, both systems have failed. No further reversion available — land immediately.


### Loss of Oil Pressure

- Confirm with Secondary Indication ... **OIL TEMP / NOISE**
  
    *if oil temp also rising — engine is losing oil. Likely seizure imminent.*
- Power ... **REDUCE**
  
    *minimize damage; lowest power that maintains flight*
- Best Field ... **LOCATE**
  
    *treat as if engine will seize*
- NRST Button ... **HOLD**
- Mayday ... **121.5 / 7700**

> *Note: Be prepared to execute Forced Landing — engine may quit at any time.*


### High Oil Temperature

- If Climbing ... **STOP CLIMB**
- RPM ... **DECREASE**
- Airspeed ... **INCREASE**
- Fuel Trim ... **+10%**
  
    *richer mixture cools the cylinders*
- Plan Diversion if Sustained ... **NEAREST SUITABLE**

### Runaway Trim


**Avionics Master** ... **OFF**


  *kills power to SV-AP-PANEL — stops all trim servo commands*

- Airspeed ... **REDUCE**
  
    *unload trim forces*
- Trim ... **MANUALLY OVERRIDE**
  
    *with stick pressure*
- Land ... **AS SOON AS PRACTICABLE**

> *Note: There is no dedicated trim circuit breaker. The avionics master is the only kill switch for the trim servos.*


## Icing / Static

### Inadvertent Icing Encounter

- Pitot Heat ... **ON**
- Icing Conditions ... **EXIT**
  
    *turn back or change altitude for warmer/colder OAT*
- Cabin Heat ... **ON**
- Defroster ... **MAX AIRFLOW**
- Engine Speed ... **INCREASE**
  
    *minimize prop blade ice buildup*
- Land ... **NEAREST AIRPORT**

> ⚠️ **WARNING:** With ¼ inch ice on leading edges, expect significantly higher stall speed.

- Wing Flaps ... **LEAVE RETRACTED**
- Approach ... **80-90 KIAS**
- Land ... **LEVEL ATTITUDE**

### Static Source Blockage


*Erroneous instrument readings suspected.*

- Alternate Static Source ... **TOGGLE ON**
  
    *panel toggle, top left*
- Airspeed ... **REFERENCE TABLE**
  
    *Cruise — 50 ft higher than normal*
  
    *Approach — 30 ft higher than normal*

## Inadvertent IMC / Upset

### 180º Turn In Clouds

- Wings ... **LEVEL ON AUTOPILOT**
- Compass Heading ... **NOTE**
- Time ... **NOTE**
- Standard Rate Turn ... **INITIATE**
  
    *60 seconds for 180º*
- Level Flight ... **MAINTAIN**
- Heading ... **RECIPROCAL CONFIRMED**

### Emergency Descent Through Clouds

- Heading ... **EAST OR WEST**
  
    *minimizes compass swings during bank changes*
- Power ... **REDUCE**
  
    *for 500-800 FPM descent*
- Trim ... **STABILIZED 80 KIAS**
- Turn Coordinator ... **MONITOR**
  
    *corrections by rudder alone; hands off the wheel*

#### Upon breaking out:

- Normal Cruising Flight ... **RESUME**

### Upset Recovery — Power / Push / Roll


**Power** ... **ADJUST**


  *nose-low: throttle back. nose-high: throttle forward.*


**Push** ... **UNLOAD**


**Roll** ... **WINGS LEVEL**


  *shortest direction; coordinated rudder*

- Recover ... **PITCH TO LEVEL**
  
    *after wings level, smoothly pitch to level flight*

### Spin Recovery — PARE


> ⚠️ **WARNING:** RV-10 is not approved for intentional spins, and Van's has not demonstrated spin recovery for the type. PARE is the universal procedure if a spin is entered inadvertently.

- P - Power ... **IDLE**
- A - Ailerons ... **NEUTRAL**
- R - Rudder ... **FULL OPPOSITE ROTATION**
- E - Elevator ... **FORWARD BRISKLY**
  
    *to break stall*

> *Note: Hold inputs until rotation stops, then neutralize rudder and recover from dive.*
