# PVWatts Solar Production Wrapper

A Python wrapper around NREL/NLR's PVWatts API that estimates annual and 
monthly solar PV energy production for a given location and system size.

## What it does

Given a location (latitude/longitude) and a system size (kW), this tool 
queries the PVWatts v8 API — which uses real historical satellite-derived 
weather data (NSRDB) rather than idealized clear-sky assumptions — and 
returns production estimates including annual output (kWh), monthly 
breakdown, and capacity factor.

## Example usage

​```python
from pv_api_wrapper import get_solar_production

result = get_solar_production(lat=17.9712, lon=-76.7936, system_capacity=5)
print(f"Annual production: {result['outputs']['ac_annual']:.2f} kWh")
# Annual production: 7866.30 kWh
​```

A 5kW system in Kingston, Jamaica produces roughly ~7,866 kWh/year under 
this model, corresponding to a capacity factor of about 18% — consistent 
with typical residential solar performance (usually 15–25%), which the 
API output itself confirms.

## Parameters and design choices

- **`tilt` / `azimuth`** (default: 20° / 180°) — south-facing, moderate 
  tilt. A common rule of thumb is tilt ≈ site latitude as a whole-year 
  compromise between summer (sun nearly overhead, favoring flatter 
  panels) and winter (sun lower, favoring steeper tilt).
- **`array_type=1`** — fixed-mount racking (no tracking system).
- **`module_type=0`** — standard crystalline silicon modules.
- **`losses=14`** — PVWatts' standard default system loss estimate 
  (wiring, soiling, shading, inverter inefficiency, etc., combined).
- **API key handling** — the key is read from an environment variable 
  (`NREL_API_KEY`), never hardcoded, so this script is safe to publish 
  and share without exposing credentials.
- **Error handling** — invalid inputs (e.g. an out-of-range latitude) 
  cause the API to return an `errors` field instead of raising an HTTP 
  failure. This wrapper checks for that and raises a `ValueError` with 
  the API's own error message, so calling code can use a standard 
  `try`/`except` block rather than manually inspecting the raw response.

## Setup

1. Get a free API key from [developer.nlr.gov](https://developer.nlr.gov/signup/)
2. Set it as an environment variable: `NREL_API_KEY`
3. `pip install requests`
4. Import and call `get_solar_production()` with your location and system size

## Background

This wrapper's output was validated against a separate clear-sky 
simulation (`pvlib-python`) for the same location — real NSRDB-weather-based 
estimates came in roughly 20–30% lower than idealized clear-sky modeling, 
which matches expected real-world solar industry patterns.