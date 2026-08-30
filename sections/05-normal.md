# Normal Procedures

> These procedures are derived from the efis-editor checklist file.
> Update the source JSON and regenerate to modify.

## Memory Items

### Memory Items — N720AK


*These items must be performed from memory before reaching for the checklist. Practice them so they are automatic.*


#### ENGINE FAILURE — A B C


**Airspeed** ... **BEST GLIDE / ONSPEED**


**Best field** ... **LOCATE / NRST**


**Checklist** ... **SYSTEM32 RESTORE**


#### ENGINE FIRE


**Fuel Pump Breakers** ... **PULL BOTH**


**Key Switch** ... **OFF**


**Fuel Selector** ... **OFF**


#### LOSS OF FUEL PRESSURE


**Fuel Pump Mode** ... **2**


**Fuel Selector** ... **OTHER TANK**


#### ELECTRICAL FIRE / SMOKE


**Key Switch** ... **OFF**


**Emergency Power Switch** ... **OFF**


**Vents** ... **OPEN**


#### LOSS OF POWER TO ELECTRONICS


**Emergency Power Switch** ... **ON**


#### RUNAWAY TRIM


**Avionics Master** ... **OFF**


#### UPSET RECOVERY — POWER PUSH ROLL


**Power** ... **ADJUST**


**Push** ... **UNLOAD**


**Roll** ... **WINGS LEVEL**


#### INADVERTENT IMC


**Wings** ... **LEVEL ON AUTOPILOT**


**180º Turn** ... **STANDARD RATE**


## Preflight

### Preflight Inspection


#### Approach:

- Gust Lock ... **REMOVE**
- Inlet Covers ... **REMOVE**
- Pitot / AoA Cover ... **REMOVE**
- AR(R)OW Documents ... **AVAILABLE**

#### Left Wing:

- Fuel Tank Vent Opening ... **CHECK**
- Fuel Tank Sump ... **DRAIN / CHECK**
- Fuel Quantity ... **CHECK VISUALLY**
- Fuel Filler Cap ... **SECURE**
- Wing Tie-Down ... **DISCONNECT**
- Wingtip Lights / Antennas ... **CHECK**
- Aileron / Flap ... **CHECK**
- Main Wheel Tire / Brake ... **CHECK**

#### Empennage:

- Baggage Door ... **CHECK / SECURE**
- Static Source Openings ... **CHECK**
- Tail Tie-Down ... **DISCONNECT**
- Control Surfaces ... **FREE / CHECK**
- Lead Weights ... **CHECK**
- ELT Antenna ... **CHECK**

#### Right Wing:

- Main Wheel Tire / Brake ... **CHECK**
- Aileron / Flap ... **CHECK**
- Wingtip Lights / Antennas ... **CHECK**
- Wing Tie-Down ... **DISCONNECT**
- Fuel Quantity ... **CHECK VISUALLY**
- Fuel Filler Cap ... **SECURE**
- Fuel Tank Sump ... **DRAIN / CHECK**
- Fuel Tank Vent Opening ... **CHECK**

#### Nose:

- Propeller and Spinner ... **CHECK**
  
    *nicks, security, oil leaks*
- Nose Wheel + Tire ... **CHECK**
- Engine Inlets / Air Intake ... **CLEAR**
  
    *look in for nests, debris, blockage*
- Engine Oil Level ... **CHECK**
  
    *Do not operate with less than 8 quarts.*
  
    *Fill to 9 quarts for extended flight.*
- Oil Door / Preheat Plug ... **STOWED / SECURE**

### Before Starting Engine

- Preflight Inspection ... **COMPLETE**
- Seats, Belts, Shoulder Harnesses ... **ADJUST AND LOCK**
- Doors ... **LOCKED**
- Circuit Breakers ... **ALL IN**
- Left Panel Switches ... **UP / NORM**
- Start Battery Select ... **BOTH**
- Avionics Master ... **OFF**
- Autopilot Switch ... **OFF**
- Key ... **ON**
- OnSpeed ... **BLINKING**
- Fuel Pump Mode ... **2, THEN 1/AUTO**
  
    *verify Pump 1 GREEN*
- ECU Select ... **ECU1**
- Fuel Quantity Indicators ... **CHECK**
- Fuel Selector ... **CYCLE BOTH TANKS**
  
    *pump running — pause on each tank until pressure steadies at 45 PSI; purges bubbles from both feed lines, proves both pickups and the selector*
- Fuel Selector ... **FULLEST TANK**
- Fuel Pressure ... **45 PSI / GREEN**
- Brakes ... **TEST AND SET**

### Starting Engine

- Propeller ... **HIGH RPM**
- Throttle (Prime) ... **2 PUMPS COLD / 1 PUMP WARM**
  
    *watch for AP indicator on EFII controller per pump*
- Throttle ... **OPEN 1/4 INCH**
  
    *If cold, wait 10s for primer fuel to evaporate*
- Propeller Area ... **CLEAR**
- Starter ... **PRESS**
  
    *release after engine starts*

#### If engine doesn't start within 5 revolutions:


  *- disengage starter,*


  *- wait ~10s for primer fuel to evaporate,*


  *- retry start.*


#### After Engine Starts:

- RPM ... **ADJUST TO 700**
  
    *reset to 700 as engine warms up*
- Oil Pressure ... **GREEN**
  
    *if not in green within 30 seconds — shut down*
- Avionics Master ... **ON**
- Autopilot Switch ... **ON**
- Strobes ... **ON**
- Alternator Current ... **VERIFY POSITIVE**
- Radios ... **SET / AWOS / ATIS**
- Altimeter ... **SET**
- Heading Indicator ... **SET**

### Before Taxi

- Wing Flaps ... **RETRACT, VERIFY UP**
- Fuel Trim ... **LEAN -10% FOR TAXI**
- Lights ... **AS REQUIRED**
- Brakes ... **TEST ON ROLL**

### Runup


> *Note: ECU controller colors: BLUE = active fuel control. GREEN = standby. RED = p-lead grounded (ignition off). GRAY = not communicating.*

- Fuel Trim ... **0%**
- Doors ... **CLOSED AND LOCKED**
- Elevator and Rudder Trim ... **TAKEOFF**
- Flight Controls ... **FREE AND CORRECT**
- Flight Instruments ... **SET**

#### Governor Cycle:

- Brakes ... **HOLD**
- Throttle ... **2000 RPM**
- Propeller Control ... **1800 RPM**
- Throttle ... **+2" MP**
  
    *let RPM stabilize*
- Propeller Control ... **HIGH RPM**

#### ECU + Fuel System Check (1600 RPM):

- Throttle ... **1600 RPM**
- Ignition (ECU p-leads) ... **CHECK**
  
    *1 OFF, Both, 2 OFF, Both*
  
    *expect ~100 RPM drop / smooth running per side*
  
    *verify active BLUE / disabled RED on EFII controller*
  
    *at Both, verify ECU1 BLUE / ECU2 GREEN*
- ECU FUEL SEL ... **PRI / SEC / PRI**
  
    *verify active GREEN, backup BLUE through transitions*
- Fuel Pump Mode ... **1 / 2 / 1/AUTO**
  
    *fuel pressure should not budge through cutover*
  
    *verify pump annunciators follow selection (active green)*
- Engine Instruments (Oil Px, Temp) ... **CHECK**
- MZ-30 Generator ... **VERIFY OUTPUT**
  
    *Bat 2 voltage charging; gen amps positive (won't show at idle)*
- Throttle ... **IDLE**

### Before Takeoff

- Fuel Gauge ... **CHECK QUANTITY**
- Fuel Pressure ... **45 PSI / GREEN**
- Fuel Trim ... **0%**
- ECU Select ... **ECU1**
- Radios, Flight Plan ... **SET**
- Transponder ... **ALT, 1200**
- Strobes ... **AS REQUIRED**
- Nav Lights ... **AS REQUIRED**
- Pitot Heat ... **AS REQUIRED**
- iPad / ForeFlight ... **CONNECTED**
  
    *Dynon WiFi — AHRS, traffic, GPS*
- Flaps / Trim ... **SET FOR TAKEOFF**

#### Takeoff Briefing — REACT:

- R - RPM ... **2700, FULL POWER**
- E - Engine gauges ... **GREEN**
- A - Airspeed ... **ALIVE**
- C - Centerline ... **TRACKING**
- T - Takeoff abort point ... **IDENTIFIED**
- Turn Direction (Engine-Out) ... **TOWARD CROSSWIND**
- Radio Call ... **MAKE**

### Normal Takeoff

- Wing Flaps ... **0º / 16º**
- Centerline ... **ALIGN**
- Power ... **FULL THROTTLE / 2700 RPM**
  
    *advance over ~5 seconds*
- Elevator ... **BACK TO LIFT NOSE**
  
    *hover nose wheel; let plane fly itself off*
- Pitch ... **ONSPEED**
- Wing Flaps ... **UP**

#### At 300 AGL:

- Propeller ... **2500 RPM**
- Climb Speed ... **START OF TONE / VY 95 KIAS**

## In Flight

### Climb

- Climb Speed ... **VY 95 KIAS to 1000 AGL**
- CHTs ... **MONITOR < 400ºF**
  
    *if approaching 400: Fuel Trim +10% or reduce climb angle*

#### At 1000 AGL — Cruise Climb:

- Airspeed ... **120 KIAS**
- Power ... **FULL THROTTLE / 2500 RPM**
- Engine Gauges ... **CHECK**

### Cruise

- Power ... **AS DESIRED**
  
    *default: full throttle / 2400 RPM*
- Flaps ... **REFLEX**
- Fuel Trim ... **0%**
- Elevator + Aileron Trim ... **ADJUST**
- Engine Gauges ... **CHECK**
- Lights ... **AS REQUIRED**

### Pre-Maneuver

- Fuel Selector ... **MORE FULL**
- Lights ... **AS REQUIRED**
- Clearing Turns ... **PERFORM**
  
    *90º L - 90º R / 180º turn*
- Maneuvering Speed ... **125 AT GROSS**

### IFR Approach Brief — WRIMTM


*Brief aloud before descent. Name the plate before W.*

- Plate ... **NAMED / CURRENT**
  
    *airport, approach + suffix, amendment, current cycle*
- Getting Established ... **STATED**
  
    *vectors / NoPT sector / HILPT / course reversal owed?*

#### W R I M T M

- Weather ... **VS MINS / RUNWAY**
  
    *ceiling + vis vs minimums, wind vs runway; altimeter source + remote-altimeter penalty if noted*
- Radios ... **TUNED / RIGHT BOX**
  
    *approach, tower/CTAF, AWOS; navaid ident if green needles*
- Instruments ... **LOADED / CRS / SOURCE**
  
    *approach + transition in GTN, final course, GPS vs VLOC driving the needle*
- Minimums ... **ALL, TOP TO BOTTOM**
  
    *sector/IAF, stepdowns, FAF crossing, DA/MDA + vis*
  
    *snowflake? apply cold-temp corrections per segment*
- Time ... **FAF-MAP IF NEEDED**
  
    *only when no fix defines the MAP*
- Missed ... **ACTION / CRS / ALT / FIX**
  
    *first action aloud, then lateral, altitude, hold fix*

### Descent

- Fuel Selector ... **MORE FULL**
- Power ... **AS DESIRED**
- Lights ... **AS REQUIRED**
- Approach Loaded ... **TRANSITION VERIFIED**
- Navaid Ident ... **DECODED ON GTN**
- GPS Integrity ... **TERM / NO LOI**

### IFR Final Gate — LAVSFT


*Established inbound, before the FAF. Verify the box — the brief was a promise, this is the audit.*

- Lateral ... **SOURCE / HSI / CRS**
  
    *GPS vs VLOC correct — the standby-localizer trap; course pointer on final approach course*
- Altitude ... **MINS BUG / MISSED ALT**
  
    *minimums bug set; altitude bug per missed-alt SOP*
- Vertical ... **GP TYPE / ARMED**
  
    *protected (LPV/GS) or advisory (+V)? advisory ignores stepdowns*
- Speed / Config ... **85 KIAS / HALF FLAPS**
  
    *from REFLEX: confirm flaps read 0 before first DOWN — a -1 start makes it a no-op*
- FMA ... **READ ALOUD**
  
    *SkyView top bar: say what it says, not what you expect*
- TDZE ... **HEIGHT AT MINS**
  
    *how high above the pavement at DA/MDA*

### Before Landing — GUMPS


#### G - Gas:

- Fuel Selector ... **FULLEST TANK**
- Fuel Pump Mode ... **1/AUTO**
- Fuel Pressure ... **45 PSI / GREEN**
- Fuel Trim ... **0%**

#### U - Undercarriage:

- Gear ... **FIXED — VERIFIED**

#### M - Mixture:

- Fuel Trim ... **0%**

#### P - Prop:

- Propeller ... **FULL FORWARD**
  
    *say it now; do it with first flap deployment*

#### S - Switches / Seatbelts:

- Seats, Belts, Harnesses ... **ADJUST AND LOCK**
- Lights ... **LANDING / TAXI**

  > *Note: Night, non-towered: key CTAF 7x for PCL (5/3 to dim); re-key on final — 15 min timer*

- Transponder ... **ALT**
- Doors ... **LATCHED**
- Brakes ... **TEST**

### Normal Landing

- Throttle ... **IDLE**
- Flaps ... **33º @ 87 KIAS**
- Propeller ... **FULL FORWARD**
- Pitch ... **ONSPEED**
- Trim ... **ADJUST**
- Throttle ... **MAINTAIN ALTITUDE / GLIDEPATH**

#### On short final:

- Throttle ... **IDLE**
- Touchdown ... **MAINS FIRST**
- Landing Roll ... **HOLD NOSE WHEEL OFF**
- Braking ... **MINIMUM REQUIRED**

## Postflight

### After Landing

- Flaps ... **UP**
- Elevator and Rudder Trim ... **TAKEOFF**
- Lights ... **AS REQUIRED**
- Pitot Heat ... **OFF**
- Transponder ... **ALT, 1200**

### Securing Airplane

- Throttle ... **IDLE**
- Hobbs + Tach Time ... **RECORD**
- Avionics Master ... **OFF**
- Autopilot Switch ... **OFF**
- Lights ... **OFF**
- Key Switch ... **OFF**
  
    *kills ECUs / fuel pumps — engine stops*
- Gust Lock ... **INSTALL**

## Non-Standard Takeoff and Landing

### Short Field Takeoff

- Flaps ... **16º**
- Power ... **FULL THROTTLE / 2700 RPM**
- Elevator ... **BACK TO LIFT NOSE**
  
    *fly off; let plane accelerate in ground effect*
- Climb Speed ... **ONSPEED / VX 80 KIAS**
  
    *until obstacles cleared*
- Flaps ... **RETRACT**

### Maximum Performance Climb

- Power ... **FULL THROTTLE / 2700 RPM**
- Airspeed ... **ONSPEED / VX 80 KIAS**
- Fuel Selector ... **MORE FULL**
- CHTs ... **MONITOR < 400ºF**

### Short Field Landing


*Drag-it-in: behind the power curve, power for descent rate, AOA for airspeed.*

- Flaps ... **33º BELOW 87 KIAS**
- Airspeed ... **SLOW TONE**
  
    *high AOA, slower than ONSPEED — touchdown speed minimized*
- Power ... **MAINTAIN DESCENT GRADIENT**
  
    *throttle controls rate of descent at this AOA*
- Trim ... **ADJUST**
- Power ... **REDUCE TO IDLE**
  
    *as obstacle is cleared*
- Touchdown ... **MAIN WHEELS FIRST**
- Brakes ... **APPLY HEAVILY**
- Flaps ... **RETRACT**

### Go Around


> *Note: Pressing "Nose Up" on the autopilot during a coupled approach engages go-around mode automatically.*

- Power ... **FULL THROTTLE / 2700 RPM**
- Pitch ... **ONSPEED**
- Flaps ... **RETRACT**
- Trim ... **SET FOR TAKEOFF**
- Climb Speed ... **VY 95 KIAS**
