# Manual Collection Plan

## Goal

Collect installation manuals, datasheets, and operating guides for every product installed on N720AK. File each to `Public/Manuals/{ATA}/` on Google Drive, register the URL in `docs/gdrive-links.md`, and link from the relevant `sys-*.md` References section.

## Workflow per item

1. **Download** the PDF from the manufacturer's website
2. **Save** to `~/Library/CloudStorage/GoogleDrive-sritchie09@gmail.com/My Drive/N720AK/Public/Manuals/{ATA}/` with a consistent filename (lowercase, hyphenated, include version/rev if applicable)
3. **Get file ID** via `xattr -p com.google.drivefs.item-id#S "/path/to/file"` (may need to wait for GDrive sync)
4. **Register** in `docs/gdrive-links.md` under the appropriate ATA section
5. **Link** from the relevant `sys-*.md` References section

## Already on file (no action needed)

- Garmin GMA 245 Pilot's Guide
- Garmin GTN 650 Pilot's Guide
- Comant CI-121 Datasheet
- Comant CI-122 Datasheet
- Artex ELT 345 Manual
- Dynon SkyView HDX Pilot's Guide (Rev Q, R)
- Dynon SkyView EMS Gauge Customization
- Dynon SkyView Third-Party Device Connection (Rev E)
- Dynon SkyView System Installation Guide (Rev AV)
- Dynon SkyView Autopilot Tuning Guide (Rev F)
- Mountain High EDS-4iP Manual + Schematic
- Vertical Power VPX Sport Install & Operating Manual (Rev G3)
- Vertical Power VPX Load Planning Worksheet
- EFII System32 Installation Manual (Rev 9-13 and 6-19)
- EFII System32 Operating Procedures (12-20)
- EFII System32 Fuel Flow & RPM Config (Rev 10-19)
- EFII System32 Initial Tuning — CSP (Rev 6-20)
- EFII System32 Upgrade Installation Manual
- EFII Bus Manager Installation Instructions
- Antisplat Aero Oil Separator / Vacuum System PDF
- TLAR Pilot Guide (v7.80)
- RV-10 Gust Lock Instructions

## Priority 1 — Core systems

### 1. EarthX ETX900 batteries
- **Find**: Installation manual and specs from earthxbatteries.com
- **Save to**: `Public/Manuals/24-Electrical/earthx-etx900-installation-manual.pdf`
- **Link from**: `sys-24-electrical.md`
- **Status**: DONE

### 2. Tosten CS Military stick grip
- **Find**: Wiring diagram and button assignment sheet from tostengrips.com or order docs
- **Save to**: `Public/Manuals/27-Flight-Controls/tosten-cs-military-wiring.pdf`
- **Link from**: `sys-27-flight-controls.md`
- **Status**: DONE

### 3. AeroLEDs Pulsar NSP wingtip lights
- **Find**: Installation manual from aeroleds.com (covers wiring, sync, dimming)
- **Save to**: `Public/Manuals/33-Lighting/aeroleds-pulsar-nsp-installation.pdf`
- **Link from**: `sys-33-lighting.md`
- **Status**: DONE

### 4. AeroLEDs AeroSun VX landing/taxi lights
- **Find**: Installation manual from aeroleds.com (covers wig-wag wiring)
- **Save to**: `Public/Manuals/33-Lighting/aeroleds-aerosun-vx-installation.pdf`
- **Link from**: `sys-33-lighting.md`
- **Status**: DONE

### 5. AeroLEDs SunTail tail light
- **Find**: Installation manual from aeroleds.com
- **Save to**: `Public/Manuals/33-Lighting/aeroleds-suntail-installation.pdf`
- **Link from**: `sys-33-lighting.md`
- **Status**: DONE

### 6. Whirlwind RV-10 propeller
- **Find**: Operating limitations, maintenance manual from whirlwindpropellers.com
- **Save to**: `Public/Manuals/84-Propeller/whirlwind-rv10-prop-manual.pdf`
- **Link from**: `sys-84-propeller.md`
- **Status**: WAITING — owner has physical copy, will scan

### 7. Andair duplex fuel valve
- **Find**: Installation instructions from andair.co.uk
- **Save to**: `Public/Manuals/28-Fuel-System/andair-duplex-valve-installation.pdf`
- **Link from**: `sys-28-fuel-system.md`
- **Status**: DONE

### 8. Aeromotive fuel pressure regulator
- **Find**: Tech specs and adjustment guide from aeromotiveinc.com (need model number from user)
- **Save to**: `Public/Manuals/28-Fuel-System/aeromotive-regulator-specs.pdf`
- **Link from**: `sys-28-fuel-system.md`
- **Status**: TODO

### 9. Walbro GSL391 fuel pump
- **Find**: Spec sheet (flow rate, pressure, wiring) — may be on holley.com (Walbro acquired by Holley/TI Automotive)
- **Save to**: `Public/Manuals/28-Fuel-System/walbro-gsl391-spec-sheet.pdf`
- **Link from**: `sys-28-fuel-system.md`
- **Status**: TODO

### 10. Matco wheels and brakes
- **Find**: Brake service manual, wheel specs from matcomfg.com (WHLWI600XLT configuration)
- **Save to**: `Public/Manuals/61-Brakes/matco-whlwi600-service-manual.pdf`
- **Link from**: `sys-61-brakes.md`
- **Status**: DONE

### 11. Beringer nosewheel
- **Find**: Maintenance manual from befrberinger.com (model specific to RV-10)
- **Save to**: `Public/Manuals/61-Brakes/beringer-nosewheel-manual.pdf`
- **Link from**: `sys-61-brakes.md`
- **Status**: DONE

### 12. OnSpeed AoA system
- **Find**: User guide and calibration documentation from flyonspeed.org
- **Save to**: `Public/Manuals/34-Navigation/onspeed-user-guide.pdf`
- **Link from**: `sys-34-onspeed.md`
- **Status**: TODO

### 13. Dynon SV-COM-C25 com panel
- **Find**: Installation guide from dynonavionics.com (part of SkyView documentation suite)
- **Save to**: `Public/Manuals/23-Communications/dynon-sv-com-c25-installation.pdf`
- **Link from**: `sys-23-communications.md`
- **Status**: DONE (customer drawing)

### 14. Vertical Power VPX Manager software
- **Find**: VPX Manager software user guide from verticalpower.com
- **Save to**: `Public/Manuals/24-Electrical/vpx-manager-software-guide.pdf`
- **Link from**: `sys-24-electrical.md`
- **Status**: DONE

## Priority 2 — Mods and accessories

### 15. Planearound 180° door latches
- **Find**: Installation instructions from planearound.com (NEW-180 kit)
- **Save to**: `Public/Manuals/52-Doors/planearound-180-latch-installation.pdf`
- **Link from**: `sys-52-doors-airframe.md`
- **Status**: SKIP — no PDF available online, installation video only

### 16. Crow Kam Lock seatbelts
- **Find**: Installation and adjustment guide from crowenterprises.com
- **Save to**: `Public/Manuals/52-Doors/crow-kam-lock-installation.pdf`
- **Link from**: `sys-52-doors-airframe.md`
- **Status**: TODO

### 17. Plane Innovations heater bypass valves
- **Find**: Installation instructions from planeinnovations.com
- **Save to**: `Public/Manuals/52-Doors/plane-innovations-heater-bypass.pdf`
- **Link from**: `sys-52-doors-airframe.md`
- **Status**: TODO

### 18. Aerosport rudder trim spring bias
- **Find**: Installation instructions from aerosportproducts.com
- **Save to**: `Public/Manuals/27-Flight-Controls/aerosport-rudder-trim-spring.pdf`
- **Link from**: `sys-27-flight-controls.md`
- **Status**: TODO

### 19. Aerosport engine mount covers
- **Find**: Installation instructions from aerosportproducts.com
- **Save to**: `Public/Manuals/71-Engine/aerosport-engine-mount-covers.pdf`
- **Link from**: `sys-71-engine.md`
- **Status**: TODO

### 20. Antisplat Aero crankcase vacuum kit
- **Find**: Vacuum kit installation instructions (separate from oil separator doc already on file)
- **Save to**: `Public/Manuals/71-Engine/antisplat-crankcase-vacuum-kit.pdf`
- **Link from**: `sys-71-engine.md`
- **Status**: TODO

### 21. Bob Archer nav antenna
- **Find**: Installation instructions (model number needed from user — likely VOR-1A or similar)
- **Save to**: `Public/Manuals/23-Communications/bob-archer-nav-antenna-installation.pdf`
- **Link from**: `sys-23-communications.md`
- **Status**: DONE

### 22. Cee Bailey windshield and windows
- **Find**: Care guide and installation instructions from ceebailey.com
- **Save to**: `Public/Manuals/52-Doors/cee-bailey-windshield-care.pdf`
- **Link from**: `sys-52-doors-airframe.md`
- **Status**: TODO

## Priority 3 — Nice to have

### 23. Lycoming IO-540 operator's manual
- **Find**: Lycoming Operator's Manual O&OM (typically Part No. 60297-10 or similar)
- **Save to**: `Public/Manuals/71-Engine/lycoming-io540-operators-manual.pdf`
- **Link from**: `sys-71-engine.md`
- **Status**: TODO

### 24. Ray Allen Pos12 flap position sensor
- **Find**: Installation/wiring sheet
- **Save to**: `Public/Manuals/27-Flight-Controls/ray-allen-pos12-installation.pdf`
- **Link from**: `sys-27-flight-controls.md`
- **Status**: TODO

### 25. Gallagher SwitcheOn remote switch
- **Find**: Wiring diagram from gallagheraviation.com
- **Save to**: `Public/Manuals/24-Electrical/gallagher-switcheon-wiring.pdf`
- **Link from**: `sys-24-electrical.md`
- **Status**: TODO

### 26. PLX SM-AFR wideband O2 gauge
- **Find**: User manual from plxdevices.com
- **Save to**: `Public/Manuals/73-EFII/plx-sm-afr-user-manual.pdf`
- **Link from**: `sys-73-efii.md`
- **Status**: TODO

### 27. Cleaveland RVAE10 axle extenders
- **Find**: Installation notes from cleavelandtool.com
- **Save to**: `Public/Manuals/61-Brakes/cleaveland-rvae10-axle-extenders.pdf`
- **Link from**: `sys-61-brakes.md`
- **Status**: TODO
