---
name: flysto-tuning
description: Audit and tune the FlySto flag thresholds and per-approach scoring limits for N720AK. Use when the user wants to review flag firing rates, recalibrate thresholds against actual flight data, or push approach scores toward "great landings" instead of "current behavior."
argument-hint: [optional starting focus, e.g., "approach scoring" or "flags" or "everything"]
user-invocable: true
---

# FlySto Tuning

Review and tune the FlySto setup for N720AK so the flags and approach scores actually drive the pilot toward better landings — instead of either firing on every flight (alarm fatigue) or never firing at all (no signal).

## Input

$ARGUMENTS

## Two distinct tuning surfaces

FlySto has two scoring systems that are configured separately:

1. **Flags** (`/flags?aircraft=nh7bk1`) — discrete per-flight events grouped into 17 categories (Taxi, Takeoff, Landing, Traffic, AGL, Acceleration, BARO, Bank, CHT, Descent, EGT, Fuel, Oil Pressure, Oil Temperature, RPM, Speed, Squawk). Each flag is yes/no per flight.

2. **Approach scoring** (`/approaches?aircraft=nh7bk1`) — every landing/T&G gets a 0-100% score from per-parameter limits configured in the **Approach limits modal**. Modal has tabs: Heights, Below 1000', Below 500', Below 200', At 50', Threshold crossing, Touchdown, Ground roll. Each parameter has Caution + Warning thresholds and per-event point penalties.

A third surface (`/insights?aircraft=nh7bk1`) is read-only and surfaces the **deviation pareto** — which flags / which approach-limit deviations fired most. Use Insights to find the *next* thing to tune.

## Core tuning philosophy

The user's goal is **better pilot, not lower scores**. Don't lock in current behavior:

- **Median ≠ correct**. If the median pilot does X and X is suboptimal, the threshold should sit *below* the median to push improvement.
- **A flag firing on >50% of flights is broken** (alarm fatigue) — but a flag firing on 0% with no real-world risk is also useless.
- **For approach scoring, aim for a distribution where**:
  - Median lands in the 80-87% range (room to improve, not insulting)
  - 90+ is achievable but rare (~10-30% of approaches)
  - 95+ is "I really nailed it" (~3-10%)
  - 100 is essentially impossible — there should always be one thing to tune
  - <70 is honestly bad and worth a debrief
- **Tighten the thing the user is bad at** so the score shouts about it. After they level up, tighten further.

## How to access the per-parameter distribution charts

This is the killer view for tuning approach scoring. Steps:

1. Open any approach detail page: `/logs/{flightId}/approaches/{idx}?view=2d`
2. Click any metric tile in the right panel (Pitch, Crab angle, IAS, etc.) — opens a popup chart
3. Click the **scatter-plot icon** ("View for all approaches" — `button[title="View for all approaches"]`)
4. The full-screen view appears with a **Parameter dropdown** at top-left and these stats: N approaches, Min, Max, **Median**, plus **RV-10 average** and **N720AK average** lines on a date-vs-value scatter
5. The Parameter dropdown lets you cycle through ~30 metrics

Use the median + RV-10-fleet-average to set thresholds. If you want to push the user above fleet average, set caution at the fleet average (or tighter).

## Common gotchas (learned the hard way)

### Pitch at 50' is NEGATIVE for an RV-10 on a stable AOA approach

A typical good RV-10 approach reads **−3° to −5° pitch at 50' AGL** (fuselage nose-down because of wing incidence + descent angle). Anything trying to enforce "pitch > 0° at 50'" will fire on 80%+ of flights. The N720AK average is around −3.3°. **Set Low Pitch limit to < −6° caution / < −8° warning** (only flag genuinely steep approaches). Set High Pitch to **> 0° caution / > +2° warning** (catch nose-up at 50' = behind on energy).

### React-controlled inputs require a real keystroke to "wake up" Save

The Approach limits modal uses React-controlled `<input>` elements. The trick we learned:

- Programmatic value updates work for *populating* fields (using native setter + `dispatchEvent('input')` + `dispatchEvent('change')`).
- But the **Save button stays disabled** until React's dirty-tracking sees a real user keystroke. Workaround: after all programmatic fills, click one input via Playwright, press a real key (e.g., `Cmd+A` then re-type the same value), then `Tab`. That enables Save.
- If a row had no scores set originally and you set them via JS, they may revert when the dropdown closes. **Verify after save** by reopening the modal.

The full programmatic helper:

```js
function realSet(input, newValue) {
  input.focus();
  const nativeSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
  nativeSetter.call(input, String(newValue));
  input.dispatchEvent(new InputEvent('input', { bubbles: true, data: String(newValue) }));
  input.dispatchEvent(new Event('change', { bubbles: true }));
  input.blur();
}
```

### Wind additive shifts IAS thresholds

The Speed additive panel adds **headwind × 50% + gust factor × 100%, clamped 6-15 kt** to all upper IAS limits during scoring. So your 50' IAS caution at 72 kts becomes 78-87 kts on a windy gusty day. Don't double-protect for wind in the base limits.

### "Touch-and-go" vs "Full-stop" both score the approach

The approach scoring runs on every landing including T&Gs. So 142 T&Gs + 69 full-stops + a few stop-and-gos = ~210 scored data points across ~60 flights. That's why you see so many points on the distribution scatter.

### Crab angle "Low" means below detection floor

In approach detail tables, crab values show as actual degrees OR the literal string `Low`. `Low` typically means < 1° or below FlySto's significance threshold. Don't parse `Low` as 0.

### KEIK/KSNY/KGXY have negative `From threshold` values

A negative `From threshold` means **touchdown short of the threshold** (undershoot). Always real safety-relevant.

### "Unstable descent path below 500'" measures deviation from 3° standard, not actual wobble

The `Unstable descent path below {500/200}'` Insights deviation has a misleading name. It computes the **vertical separation** between the actual descent trace and a standard 3° glidepath, in feet. So a smooth, monotonic 6° power-off-180 descent will show 50-80' "deviation" even though the trace is rock-stable. Genuinely unstable shelf-and-dive approaches show 100-130'+.

When triaging:
- **<100'**: usually just "you flew steeper than 3°," normal for P-O-180s. Dismiss.
- **>100'**: open the chart. If you see a shelf or a clear inflection, real debrief item. If smooth-but-steep, also dismiss.
- This deviation is **not configurable** in the limits modal — it's a built-in FlySto specialized check. You can only filter it during review.

## Workflow: full audit pass

When the user says "audit my flysto setup" or similar:

1. **Pull current Flags state** — visit `/flags?aircraft=nh7bk1&group={each}` programmatically and grab the rule text + "In X flights of 60" hit rate for each.

2. **Pull current Approach limits** — open the limits modal (click any approach tile → click Configure limits & scores icon) and dump every row's Caution/Warning/scores from each tab.

3. **Pull approach distribution stats** — for each parameter via the cross-approaches view, capture N / min / median / max.

4. **Compute hit-rate health for each flag** — anything > 30% of flights is candidate for loosening or removal; anything 0/60 with no safety value is candidate for tightening.

5. **For approach scoring, build a table** — Parameter | Median | Current Caution | Current Warning | Recommended Caution | Recommended Warning | Rationale.

6. **Show your math** — for each suggested change, explain *why* (caution should fire on top X% of approaches; warning on top Y%; what behavior the user is being pushed toward).

7. **Apply changes** — open the limits modal, programmatically fill, then a single real keystroke + Save. Verify the new score distribution shifted as predicted.

8. **Sanity-check by inspecting outliers** — pull the new top-3 approaches (the user's "best") and the bottom-decile approaches, click into each, click the score breakdown, confirm the gap reflects a real skill issue and not a config error.

## Useful URLs

| URL | What it shows |
|---|---|
| `/flags?aircraft=nh7bk1&group={category}` | Flags for one category. Categories: taxi, takeoff, landing, traffic, agl, acceleration, baro, bank, cht, descent, egt, fuel, oil-pressure, oil-temperature, rpm, speed, squawk |
| `/approaches?aircraft=nh7bk1` | Per-approach scorecard table with all metrics |
| `/insights?aircraft=nh7bk1` | Aggregate dashboard with flag/deviation pareto |
| `/insights/issues?aircraft=nh7bk1` | Sortable list of every approach-limit deviation |
| `/logs/{flightId}/approaches/{idx}?view=2d` | Approach detail with score breakdown (click "Approach score: X%") |

## Per-parameter starting recommendations for an RV-10 + AOA pilot

Reference numbers for reference. **Re-derive from current distribution rather than copying blindly** — these were last tuned for N720AK as of May 2026.

| Phase | Parameter | Caution | Warning | Notes |
|---|---|---|---|---|
| Heights | Final intercept | < 200' | < 100' | Median ~300'; push to be lined up by 200 |
| Below 500' | High IAS | > 80 kt | > 90 kt | Median 79; fleet OnSpeed ~67 kt |
| Below 500' | Low IAS | < 60 kt | < 56 kt | OnSpeed lower bound; AOA-flying floor |
| Below 500' | Max desc rate | > 1500 fpm | > 2000 fpm | Median 1121 fpm |
| Below 500' | Descent dev | > 50' | > 100' | Median 27' |
| Below 200' | High IAS | > 78 kt | > 85 kt | Median 73; bleeding to OnSpeed |
| Below 200' | Low IAS | < 60 kt | < 56 kt | OnSpeed floor |
| Below 200' | Max desc rate | > 1100 fpm | > 1400 fpm | Median 929 fpm |
| Below 200' | Descent dev | > 15' | > 25' | Tight — push precision |
| At 50' | High IAS | > 72 kt | > 78 kt | OnSpeed top |
| At 50' | Low IAS | < 60 kt | < 56 kt | OnSpeed floor |
| At 50' | High Pitch | > 0° | > +2° | Nose-up = behind on energy |
| At 50' | **Low Pitch** | **< −6°** | **< −8°** | **CRITICAL: median is −3.3°; do NOT use 0° here** |
| Threshold | High IAS | > 67 kt | > 72 kt | Median 61 |
| Threshold | Low IAS | < 55 kt | < 50 kt | Vso safety |
| Threshold | High Height | > 30' | > 50' | Median 7' |
| Touchdown | High IAS | > 62 kt | > 67 kt | Median 54 |
| Touchdown | Low IAS | < 48 kt | < 45 kt | Vso − 2 |
| Touchdown | Crab | > 2° | > 4° | Stretch goal — push to 0-2° aspiration |
| Touchdown | G-load | > 1.5 G | > 1.8 G | Median 1.20 |
| Touchdown | VS | > 250 fpm | > 400 fpm | Median 211; held-off should be ≤200 |
| Touchdown | From centerline | > 10' | > 20' | Push precision |
| Touchdown | High Pitch | > 11° | > 13° | Tail strike margin (max observed 9.8°) |
| Touchdown | **Low Pitch** | < 5° | < 3° | Median 5.4°; push held-off landings |
| Ground roll | Braking | > 0.15 G | > 0.2 G | Median 0.15 |

## Per-parameter wind additive (don't change)

```
Headwind: × 50%
Gust factor: × 100%
Min: 6 kts
Max: 15 kts
```

These are sane and match real RV-10 stable-approach physics.

## Reference: aircraft-specific numbers for N720AK (RV-10)

- **Vso (full flap stall):** ~50 KIAS
- **Vs (clean stall):** ~62-64 KIAS
- **OnSpeed approach (AOA, solo):** 65-68 KIAS
- **OnSpeed approach (heavy):** 71 KIAS
- **OnSpeed band:** 1.25× to 1.35× Vso = 62.5 - 67.5 KIAS
- **Vbg (best glide):** 87.5 KIAS at 2282 lbs
- **Vne:** 200 KIAS
- **Vno:** 174 KIAS
- **First flap extension speed:** 95 KIAS
- **Full flap speed:** 85 KIAS
- **RPM redline:** 2700
- **CHT yellow-line:** 400°F sustained, 420°F absolute (Mike Busch / Savvy)
- **Oil P normal:** 60-90 psi cruise, 25 psi idle minimum, 115 psi cold-start max
- **Oil T redline:** 245°F

The user typically flies **smooth power-off 180s** with late final intercept (200-400' AGL is normal, not late). Honor that.

## Don't change without thinking

These flags are good safety nets and should stay regardless of tuning fashion:

- 7700/7600/7500 squawk
- Bank > 45° AND AGL < 500'
- AGL < 500' AND distance to airport > 4 nm
- Remaining runway < 0' AND AGL < 50'
- Oil P > 115 psi (cold-start over-pressure)
- CHT > 435°F (real engine damage zone)
- Oil T > 245°F (redline)

## When the user says "tighten more"

Walk the ladder. After each round of changes, pull the new score distribution and check that the percentiles shifted as predicted. Common ladders:

1. Crab caution: 4° → 3° → 2° → 1° (1° = "kicked it out perfectly")
2. TD VS caution: 400 → 300 → 250 → 200 (200 = "settled, not landed")
3. TD pitch low caution: 3° → 4° → 5° → 6° (6° = held-off, mains kiss first)
4. Final intercept: 250' → 200' → 150' → 100' (100' = stable on final visual approach)
5. Centerline: 25' → 20' → 15' → 10' → 5' (5' = wingspan precision)

Tightening to the next rung should reduce the user's typical score by 2-4 points. If a tightening drops scores by 10+, it's overshot — back off one notch.

## When the user says "I'm scoring too easy"

Push to the next rung above. The right zone is "I have to work for 90".

## Output format

When done, give the user:

1. **What changed** (table: parameter | old | new | why)
2. **Predicted score distribution shift** (current p50, expected new p50)
3. **The single skill to focus on next** (from looking at the bottom-decile breakdowns — what's costing the most points across approaches?)
