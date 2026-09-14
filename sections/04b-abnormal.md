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

### Autopilot Malfunction


*Autopilot drifting, banking, or not tracking what you asked for.*


**Aircraft Control** ... **MAINTAIN**

- Mode Annunciation ... **READ IT BEFORE TOUCHING ANYTHING**

> ⚠️ **WARNING:** TRK on a coupled localizer means guidance is GONE. Dynon drops NAV to TRK silently on signal loss and does NOT recapture — NAV must be re-armed by hand.

- Downgrade One Level ... **NAV → HDG, COUPLED → BASIC**
  
  *a simpler mode that works beats hand-flying in IMC*
- Control Wheel Steering ... **HOLD DISCONNECT, FLY, RELEASE**
  
  *repositions the airplane without giving up the autopilot*
- Autopilot ... **DISCONNECT**
  
  *if downgrading does not fix it*
- Trim ... **CHECK AND RESET**
  
  *the servo may have left the airplane well out of trim*

> *Note: Manual force on the stick slips the servo clutches, so the airplane can always be overpowered.*


> *Note: If it will not disconnect → Runaway Trim (Avionics Master OFF).*


### Brake Failure


*Pedal goes soft or to the floor, or the airplane pulls on rollout.*


**Both Sides** ... **TEST AT ALTITUDE OR ON DOWNWIND**


*find out whether it is one brake or both BEFORE committing*

- Pedals ... **PUMP**
  
  *may rebuild line pressure — usually will not*
- Co-Pilot Pedals ... **TRY**
  
  *separate master cylinders on the right side*

#### Runway Choice:

- Runway ... **LONGEST AND WIDEST AVAILABLE**
  
  *width matters more than length with one brake*
- Wind ... **HEADWIND OVER CROSSWIND**
  
  *a crosswind FROM the failed side helps steering, but never take a crosswind over a headwind to get it*

#### Landing:

- Touchdown ... **SLOWEST PRACTICAL — SHORT FIELD TECHNIQUE**
- Touchdown Position ... **SIDE OF THE FAILED BRAKE**
  
  *the working brake will walk you across the runway — leave room*
- Flaps ... **LEAVE AT 33º**
  
  *aerodynamic braking — this is the OPPOSITE of short-field rollout, where flaps come up to load the wheels*
- Elevator ... **FULL AFT**
- Directional Control ... **RUDDER, THEN GOOD BRAKE IN PULSES**
  
  *alternate the working brake against opposite rudder*
- S-Turns ... **GENTLE, IF ROOM**
  
  *lengthens the effective rollout*
- Key Switch ... **OFF ONLY IF GO-AROUND NO LONGER POSSIBLE**
  
  *removes residual thrust — but it is also the engine*

> *Note: Grass beside the runway stops an airplane sooner than pavement.*


> *Note: Taxi in slowly, or shut down and get towed.*


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

### Lost Communications — IFR


#### Troubleshoot:

- Volume / Squelch / Frequency ... **CHECK**
  
    *headset jack and PTT; last assigned frequency, then the one before it*
- COM 2 / FTA-850 Handheld ... **TRY**
  
    *GTN COM 1 rides the essential bus; the handheld is the independent radio*
- Transponder ... **7600**
  
    *then listen: Guard 121.5, FSS 122.2, the navaid voice channel*

#### VMC now, or VMC encountered later:

- Continue VFR ... **LAND AS SOON AS PRACTICABLE**
  
    *§91.185(b) comes first — a suitable airport, not the nearest strip*

#### IMC — route and altitude:

- Route ... **ASSIGNED / VECTOR / EXPECTED / FILED**
  
    *A-V-E-F: last assigned; if on a vector, direct to the fix or route in that clearance; else what ATC said to expect; else as filed*
- Altitude ... **HIGHEST OF M-E-A, PER SEGMENT**
  
    *Minimum IFR altitude (MEA / MOCA / OROCA), Expected, Assigned — the highest of the three, re-checked at every segment*

#### Arrival:

- Clearance limit IS an IAF ... **DESCEND / APPROACH AT EFC — ELSE AT ETA**
  
    *hold until the EFC time or the flight-plan ETA; never start down early*
- Clearance limit NOT an IAF ... **LEAVE AT EFC — ELSE ON ARRIVAL, TO AN IAF**
  
    *then begin the approach as close to the ETA as possible*
- Approach ... **ANY PUBLISHED — FULL PROCEDURE**
  
    *own choice, no vectors are coming; fly the course reversal if charted*
- CTAF / AWOS ... **BLIND CALLS / MONITOR**
  
    *position and intentions on CTAF; lights 7 clicks; ATC is protecting the airspace on your ETA*

> *Note: Comm regained at any point: call ATC, squawk the assigned code, continue the last clearance. After landing, close the flight plan by phone or FSS.*

